from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel


class AbstractTableModel(BaseModel):
    pk: Optional[str] = None
    sk: Optional[str] = None
    ts_created: Optional[int] = None
    ts_changed: Optional[int] = None

    @abstractmethod
    def key(self):
        pass

    @abstractmethod
    def to_item(self):
        pass

    def ts_created_and_changed(self) -> dict:
        return {"ts_created": self.ts_created, "ts_changed": self.ts_changed}
