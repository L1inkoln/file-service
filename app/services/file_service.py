from fastapi import UploadFile
from typing import AsyncGenerator, Tuple
from app.storage.local import LocalStorage


class FileService:
    def __init__(self):
        self.storage = LocalStorage()

    async def upload_file(self, file: UploadFile) -> str:
        return await self.storage.save(file)

    async def download_file(
        self, filename: str
    ) -> Tuple[AsyncGenerator[bytes, None], str, int]:
        return await self.storage.get(filename)

    async def list_files(self) -> list[str]:
        return await self.storage.list()

    async def delete_file(self, filename: str) -> bool:
        return await self.storage.delete(filename)
