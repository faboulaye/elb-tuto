from datetime import datetime

import boto3
from models.abstract_table_model import AbstractTableModel
from utils.logging_utils import logger

MAX_BATCH_WRITE_ITEMS = 25


class DynamoDbRepository:
    """
    This class is used to interact with dynamodb tables
    """

    def __init__(self, table_name: str):
        logger.info("init dynamodb repositories for table %s", table_name)
        self._table_name = table_name
        self._dynamo_table = boto3.resource("dynamodb").Table(table_name)

    def get_item(self, get_kwargs: dict) -> dict:
        logger.debug(
            "get_item from table %s args: %s", self._dynamo_table.name, get_kwargs
        )
        return self._dynamo_table.get_item(**get_kwargs)

    def scan_item(self, scan_kwargs: dict) -> list:
        logger.debug(
            "scan_item from table %s args: %s", self._dynamo_table.name, scan_kwargs
        )

        done = False
        start_key = None
        result = []
        query_kwargs_copy = scan_kwargs.copy()

        while not done:
            if start_key:
                query_kwargs_copy["ExclusiveStartKey"] = start_key
            partial_data = self._dynamo_table.scan(**scan_kwargs)
            start_key = partial_data.get("LastEvaluatedKey", None)
            done = start_key is None
            result.extend(partial_data["Items"])
        return result

    def query_item(self, query_kwargs: dict) -> list:
        logger.debug(
            "query_item table name %s, %s", self._dynamo_table.name, query_kwargs
        )
        return self._dynamo_table.query(**query_kwargs)["Items"]

    def put_item(self, item: AbstractTableModel) -> dict:
        logger.debug("put_item from table %s", self._dynamo_table.name)
        item.ts_created = item.ts_changed = int(datetime.now().timestamp())
        item_in_json = item.to_item()
        self._dynamo_table.put_item(Item=item_in_json)
        return item_in_json

    def update_item(
        self,
        key: dict,
        update_expression: str,
        expression_attribute_names: dict,
        expression_attribute_values: dict,
    ) -> dict:
        ts_changed = int(datetime.now().timestamp())
        update_expression = f"{update_expression}, #ts_changed = :ts_changed"
        expression_attribute_names["#ts_changed"] = "ts_changed"
        expression_attribute_values[":ts_changed"] = ts_changed
        response = self._dynamo_table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",
        )
        return response

    def batch_put_items(self, items: list) -> list:
        response: list = []
        for chunk_items in self.slicer(items, MAX_BATCH_WRITE_ITEMS):
            request_items = {}
            put_requests = []
            for item in chunk_items:
                put_requests.append({"PutRequest": {"Item": item}})
            request_items[self._table_name] = put_requests
            response.extend(self._dynamo_table.batch_write(request_items))
        return response

    def delete_item(self, delete_kwargs: dict) -> dict:
        logger.debug(
            "delete_item from table %s args: %s", self._dynamo_table.name, delete_kwargs
        )
        return self._dynamo_table.delete_item(**delete_kwargs)

    @staticmethod
    def slicer(items: list, size) -> list:
        result: list = []
        for pos in range(0, len(items), size):
            result.append(items[pos : pos + size])
        return result
