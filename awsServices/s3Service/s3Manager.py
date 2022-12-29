import boto3
from botocore.exceptions import ClientError
from enum import Enum
import logging
import os
import requests
import sys
import threading


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


class S3Enums(Enum):
    BUCKET_NAME = 'innotter'

    def __str__(self):
        return self.value


class S3FileManager():

    def __init__(self):
        self.client = boto3.client('s3', endpoint_url="http://localhost.localstack.cloud:4566", region_name="us-west-1")
        if not S3FileManager.get_bucket(self.client):
            S3FileManager.create_bucket(self.client, S3Enums.BUCKET_NAME.value)

    @staticmethod
    def create_bucket(client, bucket_name, region="us-west-1"):
        try:
            if region is None:
                client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                client.create_bucket(Bucket=bucket_name,
                                          CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    @staticmethod
    def get_bucket(client):
        response = client.list_buckets()
        if S3Enums.BUCKET_NAME.value in response['Buckets']:
            return True
        return False

    def create_presigned_post(self, bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
        try:
            response = self.client.generate_presigned_post(Bucket=bucket_name,
                                                            Key=object_name)
            logger.info("Got presigned URL: %s", response)
            #Upload file to S3 using presigned URL
            files = { 'file': open("test.png", 'rb')}
            requests.post(response['url'], data=response['fields'], files=files)
        except ClientError:
            logger.exception(
                "Couldn't get a presigned URL for client method")
            raise
        return response

    def upload_file(self, file_name, bucket, object_name=None):
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)
        try:
            self.client.upload_file(file_name, bucket, object_name, Callback=ProgressPercentage(file_name))
        except ClientError as e:
            logging.error(e)
            return False
        return True
    