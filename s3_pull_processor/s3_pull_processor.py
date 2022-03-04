import logging
import warnings

import click
from s3_pull_processor.upload import upload_artifact
from s3_pull_processor.pull import pull_artifacts
from s3_pull_processor.artifact import Artifact

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command(help="upload artifact to S3 object storage")
@click.option("--debug", "-d", help="Enable debug logging", is_flag=True, default=False)
@click.option("--path", "-p", help="artifact absolute path", required=True, type=str)
@click.option(
    "--fake", "-f", help="create a fake artifact for test", is_flag=True, default=False
)
def upload(debug, path, fake):
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

    artifact_path = path
    if fake:
        artifact = Artifact.artifact_mock(1)[0]
        print(f"creating a fake artifact {artifact.name} at {artifact.path}")
        artifact_path = artifact.path

    upload_artifact(artifact_path)


@cli.command(
    help="start consumer, pulling artifacts from S3 and processing/importing to 3rd party application"
)
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
