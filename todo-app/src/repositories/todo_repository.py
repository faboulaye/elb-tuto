from typing import List

from pydantic import TypeAdapter

from models.todo import Todo
from repositories.dynamodb_repository import DynamoDbRepository
from utils.logging_utils import logger


class TodoRepository(DynamoDbRepository):
    def __init__(self, table_name: str):
        super().__init__(table_name)

    def get_item(self, todo_id: str) -> Todo:
        request_query = {"Key": Todo.build_todo_key(todo_id)}
        todo = super().get_item(request_query)
        return TypeAdapter(Todo).validate_python(todo)

    def get_all(self) -> List[Todo]:
        todos: list = super().scan_item({})
        logger.info("Successfully load %i todos", len(todos))
        return TypeAdapter(List[Todo]).validate_python(todos)
