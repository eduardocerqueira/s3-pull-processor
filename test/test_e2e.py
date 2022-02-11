import pytest
from s3_pull_processor.aws import AWSClient
from s3_pull_processor.artifact import Artifact
from s3_pull_processor.actions import import_to_ibutsu
from os import makedirs
import json


def test_e2e():
    """
    host A: the uploader, machine with access to the artifact file, and will upload it to S3 bucket
    host B: the consumer, machine that will consume files from S3 bucket and run an action

    simulates in the host A running s3-pull-processor upload --path /tmp/file.tar.gz
    and on host B running s3-pull-processor pull
    """
    aws = AWSClient()

    # ** host A **
    print("\n HOST A")

    # upload file to S3 bucket
    artifact = Artifact.artifact_mock(1)[0]
    assert aws.upload_file(file_path=artifact.path, file_name=artifact.name)

    # send message to SQS
    response = aws.send_message(artifact=artifact)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    # ** host B **
    print("\n HOST B")

    # read messages from SQS
    response = aws.read_message(max=1, wait=1, timeout=10)
    msg = json.loads(response["Messages"][0]["Body"])
    print(msg)

    # get msg's artifact file from S3
    path = "/tmp/s3/download"
    makedirs(path, exist_ok=True)
    assert aws.get_file(file_name=msg["name"], file_path=f"{path}/{msg['name']}")

    # run action
    import_to_ibutsu(f"{path}/{msg['path']}")

    # delete msg's artifact file from S3
    assert aws.delete_file(file_name=msg["name"])

    # delete msg from SQS
    aws.delete_message(receipt=response["Messages"][0]["ReceiptHandle"])


def test_host_uploader():
    """simulate host or pipeline generating artifacts and uploading to S3"""
    aws = AWSClient()
    artifacts = Artifact.artifact_mock(10)
    for artifact in artifacts:
        # upload file to S3 bucket
        assert aws.upload_file(file_path=artifact.path, file_name=artifact.name)
        # send message to SQS
        response = aws.send_message(artifact=artifact)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_host_consumer():
    """simulate the host consuming the SQS message, download the file from S3 bucket and import to ibutsu"""
    aws = AWSClient()

    counter = 1
    while True:
        # read messages from SQS
        response = aws.read_message(max=10, wait=1, timeout=10)

        # abort
        if "Messages" not in response or len(response) == 1:
            print("\n\nZERO messages, queue is empty!")
            break

        # process messages
        for message in response["Messages"]:
            # consume msg and run action
            msg = json.loads(message["Body"])
            print(f"\nSQS MSG :: {counter} - {msg}")

            # get msg's artifact file from S3
            path = "/tmp/s3/download"
            makedirs(path, exist_ok=True)
            assert aws.get_file(
                file_name=msg["name"], file_path=f"{path}/{msg['name']}"
            )

            # run action
            import_to_ibutsu(f"{path}/{msg['path']}")

            # delete msg's artifact file from S3
            assert aws.delete_file(file_name=msg["name"])

            # delete msg from SQS
            aws.delete_message(receipt=message["ReceiptHandle"])
            print(f"DELETED :: message {counter} - {msg}")
            counter = counter + 1

        # abort, well done! all messages consumed
        if "Messages" not in response:
            print("\n\nwell done! all messages consumed")
            break
