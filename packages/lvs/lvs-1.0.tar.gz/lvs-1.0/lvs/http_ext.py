"""
Extension to serve video stream for client(s) using browser(s)

A big thanks to Miguel's blog post that made
this flask app extension possible

https://blog.miguelgrinberg.com/post/video-streaming-with-flask
"""

import threading as th
import time
import logging

from flask import Flask, Response, render_template

from lvs.video_streamer import dataclass_objects as do
from lvs.video_streamer import video_streamer as vs

# seconds to wait before flask app goes to sleep,
# after all clients are disconnected
SLEEP_DELAY: int = 10

# limit to serving frames every x seconds
# 0.04 means serve 1 frame every 0.04 second or 25 frames per second
# if this is set to serve more fps than can be updated on `shared_frame`,
# duplicate frames will be served
FRAMES_DELAY: float = 0.04

logger = logging.getLogger(__name__)

_flask_settings: do.FlaskSettings

app = Flask(__name__)

svi: vs.SlaveVideoIter

shared_frame = None
shared_frame_lock = th.Lock()
shared_frame_requested = th.Event()
shared_frame_access_td = vs.TimeDiff()


def shared_frame_updater(sleep_delay):
    logger.debug("`shared_frame_updater` started!")
    global shared_frame
    global shared_frame_lock
    global shared_frame_requested
    global svi

    while True:
        shared_frame_requested.wait()
        while shared_frame_requested.is_set():

            # get next stream data from the server
            try:
                stream_data = next(svi)
                with shared_frame_lock:
                    shared_frame = stream_data.frame
            except StopIteration:
                with shared_frame_lock:
                    shared_frame = None
                # wait until the stream server comes back online
                time.sleep(2)
                continue

            # put the app to sleep if idle for `sleep_delay` seconds
            last_access = shared_frame_access_td.last_access_time
            if (time.time() - last_access) > sleep_delay:
                svi.release()
                shared_frame_requested.clear()


def next_frame_gen():
    global shared_frame
    global shared_frame_lock
    global shared_frame_requested
    global shared_frame_access_td

    while True:
        shared_frame_access_td.get_diff()  # update that `share_frame` was accessed

        if not shared_frame_requested.is_set():
            shared_frame_requested.set()
            # allow some time so that shared_frame becomes available
            time.sleep(2)

        got_frame = False
        with shared_frame_lock:
            if shared_frame is not None:
                frame = shared_frame.copy()
                got_frame = True

        # wait until we have a frame to serve
        if not got_frame:
            time.sleep(2)
            continue

        # Limit frames to prevent unnecessary computation by clients
        time.sleep(FRAMES_DELAY)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame.tobytes() + b'\r\n')


@app.route('/')
def index():
    global _flask_settings
    return render_template('index.html', background_color=_flask_settings.background_color)


@app.route('/video_stream')
def video_stream():
    return Response(
        next_frame_gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


def _run_flask(server_address, stream_settings):

    global svi
    svi = vs.SlaveVideoIter(server_address, do.PreStreamDataByClient(stream_settings))

    global _flask_settings
    shared_frame_updater_th = th.Thread(
        target=shared_frame_updater,
        args=(_flask_settings.sleep_delay, )
    )
    shared_frame_updater_th.setDaemon(True)
    shared_frame_updater_th.start()

    app.run(_flask_settings.ip, _flask_settings.port, _flask_settings.debug)


def run_flask(
        server_address: do.ServerAddress,
        stream_settings: do.StreamSettings,
        flask_settings: do.FlaskSettings
        ):
    logger.debug(f"Parameters received for `run_flask`:\n"
                 f"{server_address}\n{stream_settings}\n{flask_settings}")

    global _flask_settings
    _flask_settings = flask_settings

    sleep_delay = flask_settings.sleep_delay
    # reset sleep delay to a default setting if the configured setting
    # is 0, empty, or invalid
    if not sleep_delay or not isinstance(sleep_delay, int):
        flask_settings.sleep_delay = SLEEP_DELAY

    _run_flask(server_address, stream_settings)
