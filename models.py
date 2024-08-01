from pydantic import BaseModel, Field
from typing import Optional


# File storage model
class FileModel(BaseModel):
    name: str
    filename: str
    summary: Optional[str]
    path: str  # store the file path


