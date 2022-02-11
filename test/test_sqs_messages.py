import pytest
from s3_pull_processor.aws import AWSClient
from s3_pull_processor.artifact import Artifact
import json

"""
AWS SQS console: https://us-east-2.console.aws.amazon.com/sqs/v2/home?region=us-east-2#/queues
"""


def test_send_message():
    aws = AWSClient()
    artifact = Artifact.artifact_mock(1)
    response = aws.send_message(artifact=artifact[0])
    print(f"\n{response}")
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_send_multiple_messages():
    aws = AWSClient()
    artifact_list = Artifact.artifact_mock(10)

    for artifact in artifact_list:
        response = aws.send_message(artifact=artifact)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        print(f"\n{response}")


def test_read_message():
    aws = AWSClient()
    response = aws.read_message(max=1, wait=0)
    print(f"\n{response}")
    print(json.loads(response["Messages"][0]["Body"]))


def test_consume_all_messages():
    """read and delete"""
    aws = AWSClient()
    counter = 1
    while True:
        response = aws.read_message(max=10, wait=1, timeout=10)

        # abort
        if "Messages" not in response or len(response) == 1:
            print("\n\nZERO messages, queue is empty!")
            break

        # process messages
        for message in response["Messages"]:
            # consume
            msg = json.loads(message["Body"])
            print(f"\nPROCESSED :: message {counter} - {msg}")
            # delete
            aws.delete_message(receipt=message["ReceiptHandle"])
            print(f"DELETED :: message {counter} - {msg}")
            counter = counter + 1

        # abort, well done! all messages consumed
        if "Messages" not in response:
            print("\n\nwell done! all messages consumed")
            break
