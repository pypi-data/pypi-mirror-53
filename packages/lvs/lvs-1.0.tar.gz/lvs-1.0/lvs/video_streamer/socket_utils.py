__all__ = ['NoDataReceived', 'get_ipv4_tcp_socket', 'send_int',
           'recv_int', 'send_data', 'recv_data']

import pickle
import struct
import socket
from typing import Any


class NoDataReceived(Exception):
    """Raised when data is still expected but not received from the socket"""


_INT_STRUCT_FORMAT = 'i'
_INT_RECV_LEN = 4  # Integer byte size as found by struct.calcsize('i')
_MAX_BYTES_TO_RECV_DATA_CHUNKS = 4096


def get_ipv4_tcp_socket() -> socket.socket:
    """
    Returns ipv4 tcp `socket`
    :return: `socket`
    """
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_int(sock: socket.socket, number: int):
    """
    Send an integer to a `socket` using `struct.pack`
    :param sock: `socket` where `number` is to be sent
    :param number: A valid python integer
    """
    sent = 0
    data = struct.pack(_INT_STRUCT_FORMAT, number)
    while sent < _INT_RECV_LEN:
        sent += sock.send(data[sent:_INT_RECV_LEN])


def recv_int(sock: socket.socket) -> int:
    """
    Receive an integer from a `socket` using `struct.unpack`
    :param sock: `socket` to receive integer from
    :return: `int`
    """
    received_bytes = b''
    while len(received_bytes) < _INT_RECV_LEN:
        received = sock.recv(_INT_RECV_LEN - len(received_bytes))
        if not received:
            raise NoDataReceived
        received_bytes += received

    return struct.unpack('i', received_bytes)[0]


def send_data(sock: socket.socket, data: Any):
    """
    Send any picklable python object to a socket
    :param sock: `socket` where `data` is to be sent
    :param data: Any picklable python object
    """
    sent = 0
    data_bytes = pickle.dumps(data)
    data_bytes_len = len(data_bytes)
    send_int(sock, data_bytes_len)
    while sent < data_bytes_len:
        sent += sock.send(data_bytes[sent:data_bytes_len])


def recv_data(sock: socket.socket, limit=_MAX_BYTES_TO_RECV_DATA_CHUNKS) -> Any:
    """
    Receive any picklable python object over a socket
    :param sock: `socket` to receive data from
    :param limit: Receive data in `limit` byte(s) chunks
    :return: Python object of type that was sent
    """
    received = 0
    size = recv_int(sock)
    recv_len = min(size, limit)
    data = sock.recv(recv_len)
    if not data:
        raise NoDataReceived
    received += len(data)

    while received < size:
        recv_len = min(size - received, limit)
        chunk = sock.recv(recv_len)
        if not chunk:
            raise NoDataReceived
        data += chunk
        received += len(chunk)

    return pickle.loads(data)
