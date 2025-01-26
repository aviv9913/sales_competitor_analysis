from pydantic import BaseModel
from pathlib import Path


class JsonBaseModel(BaseModel):
    @classmethod
    def load_from_json_file(cls, file_path: str):
        post = cls.model_validate_json(Path(file_path).read_text(encoding="utf-8"))
        return post

    def save_to_json_file(self, file_path: str):
        Path(file_path).write_text(self.model_dump_json(indent=4), encoding="utf-8")
