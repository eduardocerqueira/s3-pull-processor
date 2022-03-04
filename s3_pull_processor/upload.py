import sys
from s3_pull_processor.aws import AWSClient
from s3_pull_processor.artifact import Artifact


def upload_artifact(artifact_path):
    aws = AWSClient()
    artifact = Artifact()
    # set unique name to the artifact, maybe can re-use the artifact name just think
    # in a situation where there are many runs uploading artifacts at the same time
    # as it is an async process.
    artifact.name = artifact.set_name()
    artifact.path = artifact_path

    print(f"artifact {artifact_path} renamed to {artifact.name}")

    try:
        # upload file to S3 bucket
        aws.upload_file(file_path=artifact.path, file_name=artifact.name)
        # send message to SQS
        response = aws.send_message(artifact=artifact)
        response["ResponseMetadata"]["HTTPStatusCode"] == 200
    except KeyboardInterrupt:
        print("[CTRL+C detected]")
        aws.abort_transaction(artifact_name=artifact.name)
        sys.exit(1)
    except Exception:
        aws.abort_transaction(artifact_name=artifact.name)
        print("*** check your AWS credentials ***")
        sys.exit(1)
