import json
from unittest.mock import Mock
from awsServices.s3Service.s3Manager import S3FileManager
from awsServices.sesService.sesEmailManager import SesEmailManager


def test_s3_service():
    client = Mock()
    d = json.loads('{"ResponseMetadata": {"RequestId": "g0SWt0EyxHzfyOKYMps669tBQ0pTQQJOVG97LL0htwxePaBR7Odg", "HTTPStatusCode": 200, "HTTPHeaders": {"content-type": "application/xml; charset=utf-8", "server": "Werkzeug/2.1.2 Python/3.10.8, hypercorn-h11", "date": "Thu, 12 Jan 2023 06:44:50 GMT, Thu, 12 Jan 2023 06:44:50 GMT", "x-amzn-requestid": "g0SWt0EyxHzfyOKYMps669tBQ0pTQQJOVG97LL0htwxePaBR7Odg", "access-control-allow-origin": "*", "connection": "close", "last-modified": "Wed, 11 Jan 2023 22:44:50 GMT", "x-amz-request-id": "A9B8684A360A2042", "x-amz-id-2": "MzRISOwyjmnupA9B8684A360A20427/JypPGXLh0OVFGcJaaO3KW/hRAqKOpIEEp", "accept-ranges": "bytes", "content-language": "en-US", "transfer-encoding": "chunked"}, "RetryAttempts": 0}, "Buckets": ["innotter", "test", "test2"], "Owner": {"DisplayName": "webfile", "ID": "bcaf1ffd86f41161ca5fb16fd081034f"}}')
    client.list_buckets.return_value = d
    assert S3FileManager.get_bucket(client) == True


def test_ses_service():
    client = Mock()
    d = json.loads('{"ResponseMetadata": {"RequestId": "ERN80CCUI0CDL221UJUHRDRMMH8C1NTS91EUQTZ9AJSMRV1EE8JT", "HTTPStatusCode": 200, "HTTPHeaders": {"content-type": "text/xml", "content-length": "288", "connection": "close", "access-control-allow-origin": "*", "access-control-allow-methods": "HEAD,GET,PUT,POST,DELETE,OPTIONS,PATCH", "access-control-allow-headers": "authorization,cache-control,content-length,content-md5,content-type,etag,location,x-amz-acl,x-amz-content-sha256,x-amz-date,x-amz-request-id,x-amz-security-token,x-amz-tagging,x-amz-target,x-amz-user-agent,x-amz-version-id,x-amzn-requestid,x-localstack-target,amz-sdk-invocation-id,amz-sdk-request", "access-control-expose-headers": "etag,x-amz-version-id", "date": "Thu, 12 Jan 2023 17:11:12 GMT", "server": "hypercorn-h11"}, "RetryAttempts": 0}}')
    client.verify_email_identity.return_value = d
    assert SesEmailManager.verify_email(client) == d