import sys

from boto3 import client
from os import getenv
from botocore.exceptions import ClientError
import json


class AWSConfException(Exception):
    """Raise AWS Credentials environment variable not found"""

    def __init__(self):
        default_message = "AWS credentials environment variables not found"
        super().__init__(default_message)


class AWSConf:
    aws_access_key_id = getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = getenv("AWS_SECRET_ACCESS_KEY")
    region_name = getenv("AWS_DEFAULT_REGION", "us-east-2")
    use_ssl = getenv("AWS_S3_SECURE_CONNECTION", "True")

    def is_cred(self):
        if (
            len(self.aws_secret_access_key) == 0
            or len(self.aws_access_key_id) == 0
            or len(self.region_name) == 0
            or len(self.use_ssl) == 0
        ):
            print("WARN: >>> AWS credentials environment variables not found <<<")
            return False
        else:
            return True


class AWSClient(AWSConf):
    sqs_queue_url = (
        "https://sqs.us-east-2.amazonaws.com/988542195534/ARTIFACT_QUEUE.fifo"
    )
    s3_bucket = "artifact-poc-bucket"

    sqs = None
    s3 = None

    if AWSConf.is_cred(AWSConf):
        sqs = client(
            service_name="sqs",
            aws_access_key_id=AWSConf.aws_access_key_id,
            aws_secret_access_key=AWSConf.aws_secret_access_key,
            region_name=AWSConf.region_name,
            use_ssl=AWSConf.use_ssl,
        )

        s3 = client(
            service_name="s3",
            aws_access_key_id=AWSConf.aws_access_key_id,
            aws_secret_access_key=AWSConf.aws_secret_access_key,
            region_name=AWSConf.region_name,
            use_ssl=AWSConf.use_ssl,
        )

    def upload_file(self, file_path, file_name):
        """upload file to S3"""
        try:
            self.s3.upload_file(
                file_path,
                self.s3_bucket,
                file_name,
                ExtraArgs={"Metadata": {"artifact_name": file_name}},
            )
            print(f"\nS3 file UPLOADED: {file_name}")
            return True
        except ClientError as ex:
            print(ex)

    def get_file(self, file_name, file_path):
        """download file from S3"""
        try:
            self.s3.download_file(self.s3_bucket, file_name, file_path)
            print(f"S3 file DOWNLOADED: {file_path}")
            return True
        except ClientError as ex:
            print(ex)

    def delete_file(self, file_name):
        """delete file from S3 bucket"""
        try:
            self.s3.delete_object(Bucket=self.s3_bucket, Key=file_name)
            print(f"S3 file DELETED: {file_name}")
            return True
        except ClientError as ex:
            print(ex)

    def send_message(self, artifact):
        """send message to SQS"""
        try:
            response = self.sqs.send_message(
                QueueUrl=self.sqs_queue_url,
                MessageGroupId="G1",
                MessageDeduplicationId=f"{artifact.name}",
                MessageAttributes={
                    "artifact_name": {
                        "DataType": "String",
                        "StringValue": f"{artifact.name}",
                    }
                },
                MessageBody=(json.dumps(artifact.__dict__)),
            )
            print(f"message sent to SQS, artifact: {artifact.name}")
            return response
        except Exception as ex:
            print(ex)
            return ex

    def read_message(self, max, wait, timeout=0):
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.sqs_queue_url,
                AttributeNames=["SentTimestamp"],
                MaxNumberOfMessages=max,
                MessageAttributeNames=["All"],
                VisibilityTimeout=timeout,
                WaitTimeSeconds=wait,
            )

            return response
        except Exception as ex:
            print(ex)

    def delete_message(self, receipt):
        """delete a message from SQS"""
        try:
            self.sqs.delete_message(QueueUrl=self.sqs_queue_url, ReceiptHandle=receipt)
        except Exception as ex:
            print(ex)

    def abort_transaction(self, artifact_name):
        """
        abort transaction to avoid S3 orphan files, situation when artifact is uploaded to S3 but
        program execution was interrupted before SQS message be dispatched.
        :param artifact_name: artifact name
        """
        if artifact_name:
            print(f"transaction aborted for artifact: {artifact_name}")
            self.delete_file(file_name=artifact_name)

    def wipe_out(self):
        response = self.s3.list_objects_v2(Bucket=self.s3_bucket)

        if "Contents" in response:
            for item in response["Contents"]:
                print("deleting file", item["Key"])
                self.delete_file(file_name=item["Key"])

        print("S3 bucket is empty")
