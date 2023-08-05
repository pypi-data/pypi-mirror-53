"""
Module to handle one or more clients requesting video stream.

Using async with intentional blocking sockets because I had issues using
async non-blocking sockets, and because it yielded much better performance
compared to threading only prototype.
"""

import asyncio as aio
import socket
import logging
import queue as q
import threading as th
from typing import List

import cv2 as cv

from .video_streamer import dataclass_objects as do
from .video_streamer import video_streamer as vs, socket_utils as su

logger = logging.getLogger(__name__)

# Max `do.StreamData` objects which the server will process and queue
# for each connected client
FRAMES_BUFFER_SIZE = 3

# Format used to encode images using `cv.imencode`
ENC = '.jpg'

# Socket the server will run on and listen for client requests
_socket: socket.socket = su.get_ipv4_tcp_socket()

_connected_clients: List[do.ClientExtras] = []

# Helpful `VideoIter` to easily get `do.StreamData` data
# from the camera or video source
_vid_iter: vs.MasterVideoIter

_server_settings: do.ServerSettings


async def _frames_q_updater():
    logger.debug("`_frames_q_updater` started!")

    global _vid_iter
    global _connected_clients

    while True:
        await aio.sleep(0)

        # Release camera or video source if no clients are connected
        if not _connected_clients:
            _vid_iter.release()
            await aio.sleep(2)
            continue

        # Read next frame and make it available to connected clients
        try:
            stream_data = next(_vid_iter)
            fps_text = str(_vid_iter.fps_estimator.get_estimate()).split('.')[0]
            approx_clients = len(_connected_clients)
            checked_clients = 0

            while checked_clients < approx_clients:
                await aio.sleep(0)

                if _connected_clients:  # Double check if clients are connected
                    try:
                        ce = _connected_clients[checked_clients]

                        # If client socket is closed, remove this client
                        if ce.sock.fileno() == -1:
                            a = ce.addr
                            logger.info(f"Client removed {a[0]+':'+str(a[1])}")
                            del _connected_clients[checked_clients]
                            raise IndexError
                        checked_clients += 1

                    # List changed, check things from the start
                    except IndexError:
                        break

                    # Client hasn't consumed existing data, move to next client
                    if ce.stream_data_q.full():
                        continue

                    custom_frame = None

                    # Apply stream settings if they were received
                    if ce.stream_settings:
                        custom_frame = vs.apply_stream_settings(
                            stream_data.frame,
                            ce.stream_settings,
                            fps_text
                        )

                    # Use stream data with default settings
                    if custom_frame is None:
                        custom_frame = stream_data.frame

                    # Ready stream data for network transmission
                    _, compressed_frame = cv.imencode(ENC, custom_frame)
                    custom_stream_data = do.StreamData(compressed_frame)
                    ce.stream_data_q.put_nowait(custom_stream_data)

        except StopIteration:
            logger.debug("`frames_q_updater` stopped!")

            # Close any connected clients
            try:
                logger.debug("Video finished. Closing remaining client connections.")
                for _ in range(len(_connected_clients)):
                    ce = _connected_clients.pop()
                    a = ce.addr
                    logger.info(f"Client removed {a[0] + ':' + str(a[1])}")
                    ce.sock.close()
            except IndexError:
                logger.debug("Closed all connected clients!")
            break


async def _serve_clients():
    logger.debug("`_serve_clients` started!")
    global _connected_clients

    while True:
        await aio.sleep(0)
        if not _connected_clients:
            await aio.sleep(2)
            continue

        approx_clients = len(_connected_clients)
        checked_clients = 0
        while checked_clients < approx_clients:
            await aio.sleep(0)

            if not _connected_clients:
                break
            try:
                ce = _connected_clients[checked_clients]
                if ce.sock.fileno() == -1:
                    del _connected_clients[checked_clients]
                    raise IndexError
                else:
                    checked_clients += 1
            except IndexError:
                break

            # Send stream data
            try:
                await aio.sleep(0)
                if not ce.stream_data_q.empty():
                    su.send_data(ce.sock, ce.stream_data_q.get_nowait())
            except (ConnectionResetError, ConnectionAbortedError, ConnectionError) as e:
                logger.error(str(e))
                if ce.sock.fileno() != -1:
                    ce.sock.close()


def _accept_connections():
    logger.debug("`_accept_connections` started!")
    global _socket
    global _connected_clients
    global _vid_iter

    while True:
        client, addr = _socket.accept()
        logger.info(f"New client connected: {addr[0]+':'+str(addr[1])}")
        try:
            client_data: do.PreStreamDataByClient = su.recv_data(client)
            su.send_data(client, do.PreStreamDataByServer(_vid_iter.vid_specs))
            _connected_clients.append(
                do.ClientExtras(
                    client, addr, q.Queue(FRAMES_BUFFER_SIZE),
                    client_data.stream_settings
                    )
            )
        except BrokenPipeError as e:
            logger.error(f"{str(e)}\nClient removed {addr[0] + ':' + str(addr[1])}")
            client.close()


async def _run_server():

    global _socket
    global _vid_iter
    global _server_settings

    s = _server_settings.source
    _vid_iter = vs.MasterVideoIter(s)

    if not _vid_iter.is_working():
        raise vs.VSError(f"Could not read from given source '{s}'")
    else:
        _vid_iter.release()  # we don't keep resources open if no clients connect

    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _socket.bind((_server_settings.ip, _server_settings.port))
    _socket.listen(_server_settings.backlog)
    logger.info(f"Server is listening on '{_server_settings.port}'")

    accept_connections_th = th.Thread(target=_accept_connections)
    accept_connections_th.setDaemon(True)
    accept_connections_th.start()

    frames_q_updater_t = aio.create_task(_frames_q_updater())
    serve_clients_t = aio.create_task(_serve_clients())

    await aio.gather(frames_q_updater_t, serve_clients_t)


def run_server(server_settings: do.ServerSettings):
    logger.debug(f"Parameters received for `run_server`:\n{server_settings}")
    global _server_settings

    _server_settings = server_settings

    aio.run(_run_server())
