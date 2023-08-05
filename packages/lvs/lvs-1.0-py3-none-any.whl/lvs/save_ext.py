"""
Extension to help in saving video stream
"""

import os
import re
import time
import logging
import datetime as dt
import pathlib as pl
import threading as th
from typing import List

import cv2 as cv

from lvs.video_streamer import dataclass_objects as do
from lvs.video_streamer import video_streamer as vs

# opencv seems to have issues in saving if not using .avi extension
VID_EXT = '.avi'
FOURCC_FORMAT = 'DIVX'
SAVE_CONTINUOUS = 'continuous'
SAVE_DETECTION = 'detection'
SAVE_TYPES: List[str] = [SAVE_CONTINUOUS, SAVE_DETECTION]

logger = logging.getLogger(__name__)

_home_path = pl.Path(os.path.expanduser('~'))
_res_path = pl.Path(__file__).parent.joinpath('res')


def _sweep_old_videos(sweep_interval: int, older_than: int, vids_dir: pl.Path):
    logger.debug("`_sweep_old_videos` started!")
    if not vids_dir.is_dir():
        raise ValueError(f"{vids_dir} is not a valid directory!")
    else:
        logger.info(f"Directory to sweep files in is '{str(vids_dir)}'")

    # targeting only files ending in our video file extension helps prevent
    # unintentional file deletions if user specifies a sensitive save directory
    pat = f"[\w\s\-]+({VID_EXT})$"
    vid_ext = re.compile(pat)  # pattern ending in `VID_EXT`
    logger.info(f"Pattern to be used to filter deletion of files: '{pat}'")

    while True:
        files = os.listdir(str(vids_dir))

        for file in files:
            path_to_file = str(vids_dir.joinpath(file))
            match = vid_ext.match(file)
            if match:

                # check if file was created earlier than specified criteria
                ctime = os.lstat(path_to_file).st_ctime
                if (time.time() - older_than) > ctime:
                    try:
                        logger.debug(f"Removing file: '{path_to_file}'")
                        os.remove(path_to_file)
                    except PermissionError:  # `file` is in use by another process
                        logger.warning(f"Could not remove file: '{path_to_file}'")

        now = time.time()
        next_sweep = now + sweep_interval
        while now < next_sweep:
            # sleep in small 5 min or lesser intervals to prevent `OverflowError`
            time.sleep(min(300, int(next_sweep-now)))
            now = time.time()


def _run_sweep_thread(sweep_interval: int, older_than: int, dir: pl.Path):
    sweep_thread = th.Thread(
        target=_sweep_old_videos,
        args=(
            sweep_interval,
            older_than,
            dir
        )
    )
    sweep_thread.setDaemon(True)
    sweep_thread.start()


def _save_stream(server_address, stream_settings, save_settings):

    classifier = pl.Path(save_settings.cascade_classifier)
    classifier_in_res = _res_path.joinpath(save_settings.cascade_classifier)

    if classifier_in_res.is_file():
        classifier_to_use = str(classifier_in_res)
        cascade_detector = cv.CascadeClassifier(classifier_to_use)
    elif classifier.is_absolute() and classifier.is_file():
        classifier_to_use = str(classifier)
        cascade_detector = cv.CascadeClassifier(classifier_to_use)
    else:
        raise ValueError("Missing cascade classifier file.\n"
                         f"'{save_settings.cascade_classifier}'' is not a file")
    logger.info(f"Loaded detection classifier: '{classifier_to_use}'")

    if save_settings.save_type not in SAVE_TYPES:
        raise TypeError(f"Invalid save type: '{save_settings.save_type}'\n"
                        f"Should be one of '{SAVE_TYPES}'")
    logger.info(f"Using save type: '{save_settings.save_type}'")

    save_dir = None
    if save_settings.save_dir:
        sd = pl.Path(save_settings.save_dir)
        if sd.is_dir():
            save_dir = sd
    elif save_settings.dir_name:
        sd = _home_path.joinpath(save_settings.dir_name)
        os.makedirs(sd, exist_ok=True)
        save_dir = sd
    if save_dir is None:
        raise TypeError("Directory to save videos is not configured properly!")
    logger.info(f"Using save directory: {save_dir}")

    if save_settings.sweep_interval > 0:
        _run_sweep_thread(save_settings.sweep_interval, save_settings.older_than, save_dir)

    vid_iter = vs.SlaveVideoIter(server_address, do.PreStreamDataByClient(stream_settings))

    fourcc = cv.VideoWriter_fourcc(*FOURCC_FORMAT)
    while True:
        try:
            data = None
            if save_settings.save_type == SAVE_CONTINUOUS:
                data = next(vid_iter)
            elif save_settings.save_type == SAVE_DETECTION:
                checked = 0
                for d in vid_iter:
                    checked += 1
                    if checked == save_settings.detection_interval:
                        checked = 0
                        gray = cv.imdecode(d.frame, cv.IMREAD_GRAYSCALE)
                        detections = cascade_detector.detectMultiScale(gray)
                        if len(detections) > 0:
                            data = d
                            break
                    else:
                        continue

            img = cv.imdecode(data.frame, cv.IMREAD_UNCHANGED)
            vid_specs: do.VideoSpecs = vid_iter.pre_stream_server_data.source_video_specs
            fps = int(vid_specs.fps)

        except (StopIteration, AttributeError):
            time.sleep(2)
            continue

        start = time.time()
        file_name = str(save_dir.joinpath(
            str(dt.datetime.now())
            .split('.')[0]  # throw milliseconds data
            .replace(' ', '_')  # remove spaces
            .replace(':', '-')  # replace invalid chars for a filename
            + VID_EXT))
        if len(img.shape) == 3:  # colored channels
            out = cv.VideoWriter(file_name, fourcc, fps, (img.shape[1], img.shape[0]))
        elif len(img.shape) == 2:  # single channel, grayscale
            out = cv.VideoWriter(file_name, fourcc, fps, (img.shape[1], img.shape[0]), 0)
        else:
            raise TypeError("Received unexpected stream type!")

        try:
            for sd in vid_iter:
                if time.time() - start < save_settings.save_duration:
                    out.write(cv.imdecode(sd.frame, cv.IMREAD_UNCHANGED))
                else:
                    break
        finally:
            out.release()


def save_stream(
        server_address: do.ServerAddress,
        stream_settings: do.StreamSettings,
        save_settings: do.SaveSettings
        ):
    logger.debug("Parameters received for `save_stream`:\n"
                 f"{server_address}\n{stream_settings}\n{save_settings}")
    try:
        _save_stream(server_address, stream_settings, save_settings)
    except (ValueError, TypeError) as e:
        raise vs.VSError(str(e))
