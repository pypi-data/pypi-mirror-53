import pathlib as pl

import click
import toml
import logging
import sys

from lvs.video_streamer import dataclass_objects as do
from lvs.video_streamer import video_streamer as vs
from lvs.stream_server import run_server
from lvs.view_ext import run_client
from lvs.http_ext import run_flask
from lvs.save_ext import save_stream, SAVE_TYPES

logger = logging.getLogger('lvs')
logger.info("\nlvs started!")

cfg_file = "res/config.toml"
cfg_file_full_path = str(pl.Path(__file__).parent.joinpath(cfg_file))
logger.info(f"Configuration file at '{str(cfg_file_full_path)}'")


def load_cfg(path: str):
    with open(path) as c:
        cfg = toml.load(c)
        return cfg


@click.group()
def cli():
    pass


@cli.command('cfg', help="Shows current configuration settings")
def show_config():
    with open(cfg_file_full_path, "r") as cfg:
        line = cfg.readline()
        while line:
            click.echo(line)
            line = cfg.readline()


@cli.command('cfg_path', help="Shows location of configuration file currently in use")
def show_config_path():
    click.echo(cfg_file_full_path)


def configure_logging(level: str, file: str):
    if level == "debug":
        log_level = logging.DEBUG
    elif level == "info":
        log_level = logging.INFO
    elif level == "critical":
        log_level = logging.CRITICAL
    else:
        log_level = logging.WARN

    logger.setLevel(log_level)

    sh = logging.StreamHandler()
    sh.setLevel(log_level)

    fh = None
    if file:
        fh = logging.FileHandler(file)
        fh.setLevel(log_level)
        fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))

    logger.addHandler(sh)
    if fh is not None:
        logger.addHandler(fh)


try:
    config = load_cfg(str(cfg_file_full_path))
except Exception as e:
    logger.error("Exiting! Failed to load configuration file!\n"+str(e))
    sys.exit(1)

try:
    configure_logging(config['log_level'], config['log_to_file'])
    server_addr = do.ServerAddress(**config['server_address'])
    server_s = do.ServerSettings(**config['server_settings'])
    stream_s = do.StreamSettings(**config['stream_settings'])
    flask_s = do.FlaskSettings(**config['flask_settings'])
    save_s = do.SaveSettings(**config['save_settings'])
except Exception as e:
    logger.error("Exiting! Configuration file contains invalid settings!\n"+str(e))
    sys.exit(1)


@cli.command('start', help="Starts the video stream server")
@click.option('--source', default=server_s.source, type=click.STRING, show_default=True)
@click.option('--ip', default=server_s.ip, type=click.STRING, show_default=True)
@click.option('--port', default=server_s.port, type=click.INT, show_default=True)
@click.option('--backlog', default=server_s.backlog, type=click.INT, show_default=True)
def run_stream_server(source, ip, port, backlog):
    new_server_s = do.ServerSettings(source, ip, port, backlog)

    # conversion required because an integer is expected if using a camera as source
    try:
        src = int(new_server_s.source)
        new_server_s.source = src
        logger.info(f"Will use camera {new_server_s.source} as source for video stream.")
    except ValueError:  # source is not a valid integer
        logger.info(f"Will use '{new_server_s.source}' file as source for video stream.")

    try:
        run_server(new_server_s)
    except vs.VSError as e:
        logger.error(str(e))


@cli.command('e_http', help="Extension to serve video stream for client(s) using browser(s)")
@click.option('--server_ip', default=server_addr.ip, type=click.STRING, show_default=True)
@click.option('--server_port', default=server_addr.port, type=click.INT, show_default=True)
@click.option('--ip', default=flask_s.ip, type=click.STRING, show_default=True, help="ip to serve http stream")
@click.option('--port', default=flask_s.port, type=click.INT, show_default=True, help="port to serve http stream")
@click.option('--sleep_delay', default=flask_s.sleep_delay, type=click.INT, show_default=True)
@click.option('--background_color', default=flask_s.background_color, type=click.STRING, show_default=True)
@click.option('--debug', default=flask_s.debug, type=click.BOOL, show_default=True)
@click.option('-G', '--grayscale/--no-grayscale', default=stream_s.grayscale, show_default=True)
@click.option('-D', '--show_datetime/--no-show_datetime', default=stream_s.show_datetime, show_default=True)
@click.option('-F', '--show_fps/--no-show_fps', default=stream_s.show_fps, show_default=True)
@click.option('--text_color', default=stream_s.text_color, nargs=3, type=click.Tuple([int, int, int]), show_default=True)
@click.option('--font_scale', default=stream_s.font_scale, type=click.INT, show_default=True)
@click.option('--thickness', default=stream_s.thickness, type=click.INT, show_default=True)
def run_http_server(
        server_ip, server_port,
        ip, port, sleep_delay, background_color, debug,
        grayscale, show_datetime, show_fps,
        text_color, font_scale, thickness,
        ):
    new_server_addr = do.ServerAddress(server_ip, server_port)
    new_stream_s = do.StreamSettings(
        grayscale, show_datetime, show_fps,
        text_color, font_scale, thickness,
    )
    new_flask_s = do.FlaskSettings(ip, port, sleep_delay, background_color, debug)

    try:
        run_flask(new_server_addr, new_stream_s, new_flask_s)
    except vs.VSError as e:
        logger.error(str(e))


@cli.command('e_view', help="Extension to show video stream from a running stream server. Press 'q' to quit when running.")
@click.option('--server_ip', default=server_addr.ip, type=click.STRING, show_default=True)
@click.option('--server_port', default=server_addr.port, type=click.INT, show_default=True)
@click.option('-G', '--grayscale/--no-grayscale', default=stream_s.grayscale, show_default=True)
@click.option('-D', '--show_datetime/--no-show_datetime', default=stream_s.show_datetime, show_default=True)
@click.option('-F', '--show_fps/--no-show_fps', default=stream_s.show_fps, show_default=True)
@click.option('--text_color', default=stream_s.text_color, nargs=3, type=click.Tuple([int, int, int]), show_default=True)
@click.option('--font_scale', default=stream_s.font_scale, type=click.INT, show_default=True)
@click.option('--thickness', default=stream_s.thickness, type=click.INT, show_default=True)
def run_stream_client(
        server_ip, server_port,
        grayscale, show_datetime, show_fps,
        text_color, font_scale, thickness,
        ):
    new_server_addr = do.ServerAddress(server_ip, server_port)
    new_stream_s = do.StreamSettings(
        grayscale, show_datetime, show_fps,
        text_color, font_scale, thickness,
    )

    try:
        run_client(new_server_addr, new_stream_s)
    except vs.VSError as e:
        logger.error(str(e))


@cli.command('e_save', help="Extension to help in saving video stream")
@click.option('--server_ip', default=server_addr.ip, type=click.STRING, show_default=True)
@click.option('--server_port', default=server_addr.port, type=click.INT, show_default=True)
@click.option('-G', '--grayscale/--no-grayscale', default=stream_s.grayscale, show_default=True)
@click.option('-D', '--show_datetime/--no-show_datetime', default=stream_s.show_datetime, show_default=True)
@click.option('-F', '--show_fps/--no-show_fps', default=stream_s.show_fps, show_default=True)
@click.option('--text_color', default=stream_s.text_color, nargs=3, type=click.Tuple([int, int, int]), show_default=True)
@click.option('--font_scale', default=stream_s.font_scale, type=click.INT, show_default=True)
@click.option('--thickness', default=stream_s.thickness, type=click.INT, show_default=True)
@click.option('--cascade_classifier', default=save_s.cascade_classifier, type=click.STRING, show_default=True)
@click.option('--detection_interval', default=save_s.detection_interval, type=click.INT, show_default=True)
@click.option('--dir_name', default=save_s.dir_name, type=click.STRING, show_default=True)
@click.option('--save_dir', default=save_s.save_dir, type=click.STRING, show_default=True)
@click.option('--save_type', default=save_s.save_type, type=click.Choice(SAVE_TYPES), show_default=True)
@click.option('--save_duration', default=save_s.save_duration, type=click.INT, show_default=True)
@click.option('--older_than', default=save_s.older_than, type=click.INT, show_default=True)
@click.option('--sweep_interval', default=save_s.sweep_interval, type=click.INT, show_default=True)
def save_video_stream(
        server_ip, server_port,
        grayscale, show_datetime, show_fps,
        text_color, font_scale, thickness,
        cascade_classifier, detection_interval,
        dir_name, save_dir, save_type, save_duration,
        older_than, sweep_interval,
        ):
    new_server_addr = do.ServerAddress(server_ip, server_port)
    new_stream_s = do.StreamSettings(
        grayscale, show_datetime, show_fps,
        text_color, font_scale, thickness,
    )
    new_save_s = do.SaveSettings(
        cascade_classifier, detection_interval,
        dir_name, save_dir, save_type, save_duration,
        older_than, sweep_interval,
    )

    try:
        save_stream(new_server_addr, new_stream_s, new_save_s)
    except vs.VSError as e:
        logger.error(str(e))


if __name__ == '__main__':
    cli()
