"""
Extension to show video stream from a running stream server
"""

import logging

import cv2 as cv

from lvs.video_streamer import dataclass_objects as do
from lvs.video_streamer import video_streamer as vs

QUIT_KEYS = (ord('q'), ord('Q'))

logger = logging.getLogger(__name__)


def _run_client(server_address, stream_settings):
    vid_iter = vs.SlaveVideoIter(
        server_address,
        do.PreStreamDataByClient(stream_settings)
    )

    if not vid_iter.is_working():
        raise vs.VSError(f"Connection to server on {server_address} failed!")

    window_name = f"Streaming from {server_address.ip}:{server_address.port}"
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    try:
        logger.info("Starting stream.")
        for stream_data in vid_iter:
            vid_iter.fps_estimator.get_estimate()
            cv.imshow(window_name, cv.imdecode(stream_data.frame, cv.IMREAD_UNCHANGED))
            key = cv.waitKey(1)
            if key in QUIT_KEYS:
                logger.info("Stopping stream on user request.")
                break
    finally:
        cv.destroyWindow(window_name)


def run_client(
        server_address: do.ServerAddress,
        stream_settings: do.StreamSettings
        ):
    logger.debug("Parameters received for `run_client`:\n"
                 f"{server_address}\n{stream_settings}")
    _run_client(server_address, stream_settings)
