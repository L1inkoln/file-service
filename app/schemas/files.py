from pydantic import BaseModel, Field
from typing import List


class FileUploadResponse(BaseModel):
    filename: str
    message: str = Field(default="File uploaded successfully")
    status: str = Field(default="success")


class MultipleFileUploadResponse(BaseModel):
    filenames: List[str]
    count: int
    message: str = Field(default="Files uploaded successfully")
    status: str = Field(default="success")


class FileDeleteResponse(BaseModel):
    filename: str
    message: str = Field(default="File deleted successfully")
    status: str = Field(default="success")


class FilesListResponse(BaseModel):
    files: List[str]
