from enum import Enum


class TodoStatus(str, Enum):
    OPEN = "open"
    PENDING = "pending"
    BLOCKED = "blocked"
    DONE = "done"
