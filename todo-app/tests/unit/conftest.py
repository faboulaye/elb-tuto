import os

import boto3
import pytest
from moto import mock_dynamodb

os.environ["DYNAMODB_TABLE"] = "src"
os.environ["AWS_DEFAULT_REGION"] = "eu-west-3"

table_name = "src"


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def dynamodb(aws_credentials):
    with mock_dynamodb():
        yield boto3.resource("dynamodb")


@pytest.fixture()
def first_mock_data() -> dict:
    return {
        "pk": "SAMPLE_TODO#FIRST_ITEM",
        "sk": "SAMPLE_TODO#FIRST_ITEM",
        "id": "FIRST_ITEM",
        "value": "FIRST_ITEM",
        "ts_created": 111,
        "ts_changed": 111,
    }


@pytest.fixture
def dynamodb_table(dynamodb):
    """Create a DynamoDB src table fixture."""

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "pk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "pk", "AttributeType": "S"},
            {"AttributeName": "sk", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )
    # table.meta.client.get_waiter(table_name).wait(TableName=table_name)
    yield


@pytest.fixture()
def init_table(dynamodb, dynamodb_table, first_mock_data):
    dynamodb.Table(table_name).put_item(Item=first_mock_data)
