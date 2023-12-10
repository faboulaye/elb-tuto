from models.abstract_table_model import AbstractTableModel


class SampleModel(AbstractTableModel):
    id: str
    value: str

    def key(self):
        return {"pk": f"SAMPLE_MODEL#{self.id}", "sk": f"SAMPLE_MODEL#{self.id}"}

    def to_item(self):
        return {
            **self.key(),
            "id": self.id,
            "value": self.value,
            **self.ts_created_and_changed(),
        }
