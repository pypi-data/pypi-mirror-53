__all__ = ['VSError', 'TimeDiff', 'FpsEstimator', 'MasterVideoIter',
           'SlaveVideoIter', 'apply_stream_settings']

import abc
import datetime
import time
from typing import Union

import cv2 as cv
import numpy as np

from . import socket_utils as su
from . import dataclass_objects as do


class VSError(Exception):
    """Base exception class for this package"""


class TimeDiff:
    """
    Once instantiated, calling `get_diff()` on the instance will return
    time difference between last two calls to `get_diff()` method
    """

    def __init__(self):
        self._time_now: float = time.monotonic()
        self._last_known_diff: float = 0
        self._last_access_time: float = time.time()

    @property
    def last_known_diff(self) -> float:
        return self._last_known_diff

    @property
    def last_access_time(self):
        return self._last_access_time

    def get_diff(self) -> float:
        self._last_access_time = time.time()
        time_now, self._time_now = self._time_now, time.monotonic()
        self._last_known_diff = self._time_now - time_now
        return self._last_known_diff

    def __str__(self):
        if not self._last_known_diff:
            return "Last known difference unknown. " \
                   "get_diff() hasn't been called yet!"
        return "Last known difference between calls to get_diff() " \
               f"is '{self._last_known_diff:.3f}' seconds."


class FpsEstimator:
    """
    Once instantiated, calling `get_estimate()` on the instance will return
    estimated frames per given interval based on the time difference
    between last two calls to `get_estimate()` method
    """

    def __init__(self):
        self._td: TimeDiff = TimeDiff()
        self._last_known_estimate: float = 0
        self._last_known_estimate_interval: float = 0

    @property
    def last_known_estimate(self) -> float:
        return self._last_known_estimate

    def get_estimate(self, interval: float = 1) -> float:
        self._last_known_estimate_interval = interval
        td = self._td.get_diff()
        if td > 0:
            self._last_known_estimate = interval / td
        return self._last_known_estimate

    def __str__(self):
        if not self._last_known_estimate:
            return "Last known estimate unknown. " \
                   "get_estimate() hasn't been called yet!"
        return f"Last known estimate per '{self._last_known_estimate_interval}'" \
               f" second(s) interval is '{self._last_known_estimate:.0f}' fps"


class VideoIterABC(abc.ABC):

    def __init__(self):
        self.fps_estimator = FpsEstimator()

    def __iter__(self):
        return self

    @abc.abstractmethod
    def __next__(self) -> do.StreamData:
        pass

    def is_working(self) -> bool:
        try:
            self.__next__()
        except StopIteration:
            return False
        return True


class MasterVideoIter(VideoIterABC):
    """To iterate video from camera or video file frame by frame"""

    def __init__(self, source: Union[int, str]):
        VideoIterABC.__init__(self)
        self._source = source
        self._vid_specs = None
        self._vid_cap = None

    @property
    def vid_specs(self):
        if self._vid_specs is None:
            self._open_cap()
            self.release()
        return self._vid_specs

    def __next__(self) -> do.StreamData:
        try:
            if self._vid_cap is None:
                self._open_cap()
            frame = self._read_frame()
        except VSError:
            self.release()
            raise StopIteration
        return do.StreamData(frame)

    def _open_cap(self) -> None:
        if self._vid_cap is None:
            self._vid_cap = cv.VideoCapture(self._source)
            self._vid_specs = get_video_capture_specs(self._vid_cap)
        if not self._vid_cap.isOpened():
            raise VSError("Failed to open video capture "
                          f"for video source: '{self._source}'")

    def _read_frame(self) -> np.ndarray:
        ret, frame = self._vid_cap.read()
        if not ret:
            raise VSError("Failed to read next frame!")
        return frame

    def release(self):
        if self._vid_cap is not None:
            self._vid_cap.release()
        self._vid_cap = None


class SlaveVideoIter(VideoIterABC):
    """To iterate video received over socket connection frame by frame"""

    def __init__(self, server_addr: do.ServerAddress, pre_data: do.PreStreamDataByClient):
        VideoIterABC.__init__(self)
        self._server_addr = server_addr
        self._pre_stream_client_data = pre_data
        self._pre_stream_server_data = None
        self._socket = None

    @property
    def pre_stream_server_data(self) -> do.PreStreamDataByServer:
        if self._pre_stream_server_data is None:
            self._connect_to_server()
            self.release()
        return self._pre_stream_server_data

    def _connect_to_server(self):
        if self._socket is None:
            self._socket = su.get_ipv4_tcp_socket()
            self._socket.connect((self._server_addr.ip, self._server_addr.port))
            su.send_data(self._socket, self._pre_stream_client_data)
            self._pre_stream_server_data = su.recv_data(self._socket)
        elif self._socket.fileno() == -1:
            raise VSError(f"Connection to '{self._server_addr.ip}:"
                          f"{self._server_addr.port}' is closed!")

    def __next__(self) -> do.StreamData:
        try:
            self._connect_to_server()
        except (VSError, ConnectionRefusedError):
            self._socket = None
            raise StopIteration
        try:
            stream_data = su.recv_data(self._socket)
        except (su.NoDataReceived, ConnectionResetError, ConnectionAbortedError):
            self.release()
            raise StopIteration
        return stream_data

    def release(self):
        if self._socket is not None:
            self._socket.close()
        self._socket = None


def get_video_capture_specs(cap: cv.VideoCapture) -> do.VideoSpecs:
    if not isinstance(cap, cv.VideoCapture):
        raise TypeError
    return do.VideoSpecs(
        width=cap.get(cv.CAP_PROP_FRAME_WIDTH),
        height=cap.get(cv.CAP_PROP_FRAME_HEIGHT),
        fps=cap.get(cv.CAP_PROP_FPS)
    )


def apply_stream_settings(frame: np.ndarray, stream_settings: do.StreamSettings, fps_text: str) -> np.ndarray:
    img = frame.copy()
    if stream_settings.grayscale:
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    assert len(stream_settings.text_color) == 3
    clr = tuple(stream_settings.text_color)

    fs = stream_settings.font_scale
    thic = stream_settings.thickness

    pos = ((int)(0.01 * img.shape[0]), (int)(0.05 * img.shape[1]))
    if stream_settings.show_datetime:
        text = str(datetime.datetime.now()).split('.')[0]
        cv.putText(img, text, pos, cv.FONT_HERSHEY_SIMPLEX, fs, clr, thic, cv.LINE_AA)
        pos = (int(0.01 * img.shape[0]), int(pos[1] + (0.05 * img.shape[1])))

    if stream_settings.show_fps:
        cv.putText(img, fps_text, pos, cv.FONT_HERSHEY_SIMPLEX, fs, clr, thic, cv.LINE_AA)

    return img
