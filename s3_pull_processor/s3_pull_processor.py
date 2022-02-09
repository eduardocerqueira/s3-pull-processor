import logging
import warnings

import click
from upload import upload_artifact
from pull import pull_artifacts

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command(help="upload data from object storage")
@click.option("--debug", "-d", help="Enable debug logging", is_flag=True, default=False)
@click.option("--path", "-p", help="artifact absolute path", required=True, type=str)
def upload(debug, path):
    logging.basicConfig(
        format="%(asctime)s [%(levelname)8s] [%(threadName)20s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if debug else logging.INFO,
    )

    def custom_formatwarning(msg, *args, **kwargs):
        # ignore everything except the message
        return str(msg)

    warnings.formatwarning = custom_formatwarning
    warnings.simplefilter("default")
    logging.captureWarnings(True)

    upload_artifact(path)


@cli.command(help="pull data from object storage")
@click.option("--debug", "-d", help="Enable debug logging", is_flag=True, default=False)
def pull(debug):
    logging.basicConfig(
        format="%(asctime)s [%(levelname)8s] [%(threadName)20s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if debug else logging.INFO,
    )

    def custom_formatwarning(msg, *args, **kwargs):
        # ignore everything except the message
        return str(msg)

    warnings.formatwarning = custom_formatwarning
    warnings.simplefilter("default")
    logging.captureWarnings(True)

    pull_artifacts()


if __name__ == "__main__":
    cli()
