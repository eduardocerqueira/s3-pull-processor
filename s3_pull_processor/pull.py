import sys
from s3_pull_processor.aws import AWSClient
from s3_pull_processor.artifact import Artifact
from s3_pull_processor.actions import import_to_ibutsu
import json
from os import makedirs
import os


def pull_artifacts():
    try:
        print("start consumer, pulling artifacts from SQS and S3...")
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
                # consume SQS msg and create artifact object
                msg = json.loads(message["Body"])
                artifact = Artifact()
                artifact.name = msg["name"]
                artifact.path = msg["path"]

                print(
                    f"\n>> SQS MSG :: CONSUMED :: {counter} - name: {artifact.name} path: {artifact.path}"
                )

                # get msg's artifact file from S3
                path = "/tmp/s3/download"
                makedirs(path, exist_ok=True)
                aws.get_file(
                    file_name=artifact.name, file_path=f"{path}/{artifact.name}"
                )

                # run action
                import_to_ibutsu(f"{path}/{artifact.name}")

                # delete local file
                if os.path.exists(f"{path}/{msg['name']}"):
                    os.remove(f"{path}/{msg['name']}")
                    print(f"local file deleted: {path}/{msg['name']}")

                # delete msg's artifact file from S3
                aws.delete_file(file_name=msg["name"])

                # delete msg from SQS
                aws.delete_message(receipt=message["ReceiptHandle"])
                print(
                    f">> SQS MSG :: DELETED :: {counter} - name: {artifact.name} path: {artifact.path}"
                )
                counter = counter + 1

            # abort, well done! all messages consumed
            if "Messages" not in response:
                print("\n\nwell done! all messages consumed")
                break
    except KeyboardInterrupt:
        print("[CTRL+C detected]")
        sys.exit(1)
    except Exception:
        print("*** check your AWS credentials ***")
        sys.exit(1)
