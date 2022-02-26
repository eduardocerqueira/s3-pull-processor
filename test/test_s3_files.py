import pytest
from s3_pull_processor.aws import AWSClient
from s3_pull_processor.artifact import Artifact
from os import makedirs

"""
AWS S3 console: https://s3.console.aws.amazon.com/s3/buckets/artifact-poc-bucket?region=us-east-2&tab=objects
"""


def test_upload_file():
    """Upload files to S3 bucket"""

    aws = AWSClient()
    artifacts = Artifact().artifact_mock(5)

    for artifact in artifacts:
        aws.upload_file(file_path=artifact.path, file_name=artifact.name)

    assert True


def test_download_file():
    """Upload and download file"""
    aws = AWSClient()
    artifacts = Artifact().artifact_mock(1)
    path = "/tmp/s3/download"
    makedirs(path, exist_ok=True)

    for artifact in artifacts:
        aws.upload_file(file_path=artifact.path, file_name=artifact.name)
        aws.get_file(file_name=artifact.name, file_path=f"{path}/{artifact.name}")

    assert True


def test_delete_file():
    """Upload and delete several files"""
    aws = AWSClient()
    artifacts = Artifact().artifact_mock(5)

    for artifact in artifacts:
        aws.upload_file(file_path=artifact.path, file_name=artifact.name)
        aws.delete_file(file_name=artifact.name)

    assert True


def test_s3_delete_all_objects():
    aws = AWSClient()
    aws.wipe_out()
