__all__ = ['ServerAddress', 'ServerSettings', 'FlaskSettings',
           'PreStreamDataByServer', 'PreStreamDataByClient',
           'StreamSettings', 'SaveSettings', 'VideoSpecs']

import dataclasses as dc
import socket
import queue as q
from typing import Union, List, Tuple

import numpy as np


@dc.dataclass
class ServerAddress:
    ip: str
    port: int


@dc.dataclass
class ServerSettings:
    source: Union[int, str]
    ip: str
    port: int
    backlog: int


@dc.dataclass
class FlaskSettings:
    ip: str
    port: int
    sleep_delay: int
    background_color: str
    debug: bool


@dc.dataclass
class StreamSettings:
    grayscale: bool

    # text-options
    show_datetime: bool
    show_fps: bool
    text_color: List[int]
    font_scale: float
    thickness: int


@dc.dataclass
class SaveSettings:

    # detection-options
    cascade_classifier: str
    detection_interval: int

    # save-options
    dir_name: str
    save_dir: str
    save_type: str
    save_duration: int

    # delete options
    older_than: int
    sweep_interval: int


@dc.dataclass
class VideoSpecs:
    """Source video/camera specifications"""

    width: float
    height: float
    fps: float


@dc.dataclass
class PreStreamDataByClient:
    """Useful info that the server shall receive before the stream starts"""

    stream_settings: StreamSettings


@dc.dataclass
class PreStreamDataByServer:
    """Useful info that the server shall provide before the stream starts"""

    source_video_specs: VideoSpecs


@dc.dataclass
class StreamData:
    """Datatype to be used for video stream"""

    frame: np.ndarray

    def __copy__(self):
        return StreamData(self.frame.copy())


@dc.dataclass
class ClientExtras:
    """To store stuff associated with client helpful for a server"""

    sock: socket.socket
    addr: Tuple[str, int]
    stream_data_q: q.Queue
    stream_settings: StreamSettings = None
