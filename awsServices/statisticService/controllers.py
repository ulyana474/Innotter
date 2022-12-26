import boto3
from botocore.exceptions import ClientError
import logging
import os


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


credentials = {
    "ENDPOINT_URL": os.environ.get("ENDPOINT_URL", ""),
    "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID", ""),
    "AWS_DEFAULT_REGION": os.environ.get("AWS_DEFAULT_REGION", ""),
    "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
}

def get_resource():
    resource = boto3.resource(
        'dynamodb',
        endpoint_url=credentials.get("ENDPOINT_URL"),
        region_name=credentials.get("AWS_DEFAULT_REGION")
    )
    return resource


def get_client():
    client = boto3.client(
        'dynamodb',
        endpoint_url=credentials.get("ENDPOINT_URL"),
        region_name=credentials.get("AWS_DEFAULT_REGION")
    )
    return client


def get_table():
    resource = get_resource()
    table = resource.Table("Pages")
    return table


def create_table():
    dynamodb = get_client()
    try:
        # Create the DynamoDB table.
        table = dynamodb.create_table(
            TableName='Pages',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    except dynamodb.exceptions.ResourceInUseException:
        resource = get_resource()
        table = resource.Table("Pages")
    except ClientError:
        logger.exception('Could not create the table.')

    return table
  
def get_statistics(page_id):
    table = get_table()
    page = table.get_item(Key={"id": page_id})
    return page


def update_item(page_id, field, increase=False):
    value = 1
    if not increase:
        value = -1
    query = f'ADD {field} :increase'
    table = get_table()
    response = table.update_item(Key={"id": page_id},
                                    UpdateExpression=query,
                                    ExpressionAttributeValues = {':increase': value},
                                    ReturnValues = 'UPDATED_NEW')
    return response


def put_item(page_id):
    table = get_table()
    response = table.put_item(
        Item={
            'id': page_id,
            'likes': 0,
            'posts': 0,
            'followers': 0,
        }
    )
    return response

