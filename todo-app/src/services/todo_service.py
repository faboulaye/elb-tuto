import uuid
from typing import List

from error.not_found_error import NotFoundError
from models.todo import Todo
from models.todo_status import TodoStatus

from repositories.todo_repository import TodoRepository
from utils.logging_utils import logger


class TodoService:
    def __init__(self, todo_table: str):
        logger.debug("init src service")
        self._todo_repository: TodoRepository = TodoRepository(todo_table)

    def save(self, todo: Todo) -> Todo:
        todo.id = str(uuid.uuid4())
        todo.status = TodoStatus.OPEN
        response = self._todo_repository.put_item(todo)
        logger.info("Successfully saved src %s", response)
        return todo

    def update(self, todo_id: str, todo: Todo) -> Todo:
        old_todo: Todo = self.get(todo_id)
        todo.id = todo_id
        request = {"Item": todo.dict()}
        response = self._todo_repository.update_item(todo_id, todo)
        logger.info("Successfully updated src %s", response)
        return todo

    def delete(self, todo_id: str) -> Todo:
        todo: Todo = self.get(todo_id)
        request_item = {"Key": {"id": todo.id, "created_at": todo.created_at}}
        response = self._todo_repository.delete_item(request_item)
        logger.info("Successfully delete src %s", response)
        return todo

    def get(self, todo_id: str) -> Todo:
        result: Todo = self._todo_repository.get_item(todo_id)
        if not result:
            raise NotFoundError(message=f"Failed to find src with id {todo_id}")
        return result

    def list(self) -> List[Todo]:
        todos: list[Todo] = self._todo_repository.get_all()
        logger.info("Successfully load %i todos", len(todos))
        return todos
