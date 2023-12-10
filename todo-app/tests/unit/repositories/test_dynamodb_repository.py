import pytest
from repositories.dynamodb_repository import DynamoDbRepository
from unit.models.sample_model import SampleModel


@pytest.fixture()
def dynamodb_repository(init_table) -> DynamoDbRepository:
    return DynamoDbRepository("src")


@pytest.fixture()
def mock_data() -> dict:
    return {
        "pk": "SAMPLE_TODO#FOOBAR",
        "sk": "SAMPLE_TODO#FOOBAR",
        "id": "FOOBAR",
        "value": "FOOBAR",
        "ts_created": 111,
        "ts_changed": 111,
    }


def test_get_item(dynamodb_repository, first_mock_data):
    res = dynamodb_repository.get_item(
        {"Key": {"pk": "SAMPLE_TODO#FIRST_ITEM", "sk": "SAMPLE_TODO#FIRST_ITEM"}}
    )
    assert first_mock_data == res["Item"]


def test_scan_item(dynamodb_repository, first_mock_data):
    res = dynamodb_repository.scan_item({})
    assert len(res) == 1
    assert res[0]["pk"] == first_mock_data["pk"]


def test_query_item(dynamodb_repository):
    res = dynamodb_repository.query_item(
        {
            "KeyConditionExpression": "pk = :pk",
            "ExpressionAttributeValues": {":pk": "SAMPLE_TODO#FIRST_ITEM"},
        }
    )
    assert len(res) == 1


def test_put_item(dynamodb_repository, mock_data):
    data = SampleModel(id="foobar", value="foobar")
    res = dynamodb_repository.put_item(data)
    assert res["pk"] == "SAMPLE_MODEL#foobar"
    assert res["sk"] == "SAMPLE_MODEL#foobar"


def test_update_item(dynamodb_repository):
    res = dynamodb_repository.update_item(
        {"pk": "SAMPLE_TODO#FIRST_ITEM", "sk": "SAMPLE_TODO#FIRST_ITEM"},
        "SET #value = :new_value",
        {"#value": "value"},
        {":new_value": "new value"},
    )
    assert res["Attributes"]["value"] == "new value"


def test_delete_item(dynamodb_repository):
    res = dynamodb_repository.delete_item(
        {
            "Key": {"pk": "SAMPLE_TODO#FIRST_ITEM", "sk": "SAMPLE_TODO#FIRST_ITEM"},
            "ReturnValues": "ALL_OLD",
        }
    )
    assert res["Attributes"]["pk"] == "SAMPLE_TODO#FIRST_ITEM"


def test_slicer():
    res: list = DynamoDbRepository.slicer([1, 2, 3, 4, 5], 2)
    assert res == [[1, 2], [3, 4], [5]]
