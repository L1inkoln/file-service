from pathlib import Path
from typing import AsyncGenerator, Tuple
from fastapi import HTTPException, status, UploadFile
import aiofiles
import aiofiles.os
import mimetypes
from app.config import settings
from app.storage.base import BaseStorage


class LocalStorage(BaseStorage):
    def __init__(self):
        self.storage_path = Path(settings.storage_path)
        self.storage_path.mkdir(exist_ok=True, parents=True)

    async def save(self, file: UploadFile) -> str:
        """
        Save an uploaded file asynchronously.
        """
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename cannot be empty",
            )

        file_path = self.storage_path / file.filename

        if file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File already exists",
            )

        # Асинхронная запись файла по кусочкам (1 MB)
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                await buffer.write(chunk)

        return file.filename

    async def get(self, file_id: str) -> Tuple[AsyncGenerator[bytes, None], str, int]:
        """
        Get a file for downloading.
        """
        if not file_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File ID cannot be empty",
            )

        file_path = self.storage_path / file_id

        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found",
            )

        file_size = file_path.stat().st_size
        content_type = self._guess_content_type(file_path)

        async def file_generator() -> AsyncGenerator[bytes, None]:
            async with aiofiles.open(file_path, "rb") as file:
                while chunk := await file.read(1024 * 1024):
                    yield chunk

        return file_generator(), content_type, file_size

    async def list(self) -> list[str]:
        """
        List all files in storage.
        """
        return [f.name for f in self.storage_path.iterdir() if f.is_file()]

    async def delete(self, file_id: str) -> bool:
        """
        Delete a file by ID (filename).
        """
        if not file_id:
            return False

        file_path = self.storage_path / file_id
        if not file_path.exists():
            return False

        await aiofiles.os.remove(file_path)
        return True

    def _guess_content_type(self, file_path: Path) -> str:
        """
        Guess the MIME type based on file extension.
        """
        content_type, _ = mimetypes.guess_type(file_path)
        return content_type or "application/octet-stream"
