from pydantic import Field

from models.abstract_table_model import AbstractTableModel
from models.todo_status import TodoStatus


class Todo(AbstractTableModel):
    id: str = Field(None, description="Todo identifier")
    title: str = Field(None, description="title")
    description: str = Field(None, description="Todo description")
    author: str = Field(None, description="Author of Todo")
    status: TodoStatus = Field(None, description="Todo status")

    @staticmethod
    def build_todo_key(todo_id: str):
        return {"pk": f"TODO#{todo_id}", "sk": f"TODO#{todo_id}"}

    def key(self):
        return Todo.build_todo_key(self.id)

    def to_item(self):
        return {
            **self.key(),
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "status": self.status,
            **self.ts_created_and_changed(),
        }
