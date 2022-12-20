import os
import boto3

credentials = {
    "ENDPOINT_URL": os.environ.get("ENDPOINT_URL", ""),
    "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID", ""),
    "AWS_DEFAULT_REGION": os.environ.get("AWS_DEFAULT_REGION", ""),
    "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
}

def get_resource():
    resource = boto3.resource(
    'dynamodb',
    endpoint_url=credentials.get("ENDPOINT_URL", ""),
    aws_access_key_id=credentials.get("AWS_ACCESS_KEY_ID", ""),
    aws_secret_access_key=credentials.get("AWS_SECRET_ACCESS_KEY", ""),
    region_name=credentials.get("AWS_DEFAULT_REGION", ""))
    return resource

def get_client():
    client = boto3.client(
    'dynamodb',
    endpoint_url=credentials.get("ENDPOINT_URL", ""),
    aws_access_key_id=credentials.get("AWS_ACCESS_KEY_ID", ""),
    aws_secret_access_key=credentials.get("AWS_SECRET_ACCESS_KEY", ""),
    region_name=credentials.get("AWS_DEFAULT_REGION", ""))
    return client

def get_table():
    client = get_client()
    try:
        dynamodb_table = client.create_table(
            TableName='Pages',
            KeySchema=[
                {
                    'AttributeName': 'Page',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Page',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
        )
    except client.exceptions.ResourceInUseException:

        resource = get_resource()
        dynamodb_table = resource.Table("Pages")
    return dynamodb_table

def get_item():
        table = get_table()
        response = table.get_item(
            Key={'AttributeName': {'S': 'Page'}}
        )

        return response

def update_item(page: str):
    table = get_table()
    response = table.update_item(
        Item={
            'Page': page
        }
    )

    return response


def put_item(page: str):
    table = get_table()
    response = table.put_item(
        Item={
            'Page': page
        }
    )

    return response

def delete_item(page: str):
    table = get_table()
    response = table.delete_item(
        Item={
            'Page': page
        }
    )

    return response