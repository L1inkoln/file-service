from pathlib import Path
from typing import AsyncGenerator, Tuple
from fastapi import HTTPException, status, UploadFile
from app.config import settings
from app.storage.base import BaseStorage


class LocalStorage(BaseStorage):
    def __init__(self):
        self.storage_path = Path(settings.storage_path)
        self.storage_path.mkdir(exist_ok=True, parents=True)

    async def save(self, file: UploadFile) -> str:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename cannot be empty",
            )

        file_path = self.storage_path / file.filename

        if file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="File already exists"
            )

        # Используем асинхронную запись файла
        with open(file_path, "wb") as buffer:
            while content := await file.read(1024 * 1024):  # Читаем по 1MB
                buffer.write(content)

        return file.filename

    async def get(self, file_id: str) -> Tuple[AsyncGenerator[bytes, None], str, int]:
        if not file_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File ID cannot be empty",
            )

        file_path = self.storage_path / file_id

        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )

        # Получаем информацию о файле
        file_size = file_path.stat().st_size
        content_type = self._guess_content_type(file_path)

        # Создаем генератор для потокового чтения файла
        async def file_generator() -> AsyncGenerator[bytes, None]:
            with open(file_path, "rb") as file:
                while chunk := file.read(1024 * 1024):  # Читаем по 1MB
                    yield chunk

        return file_generator(), content_type, file_size

    async def list(self) -> list[str]:
        return [f.name for f in self.storage_path.iterdir() if f.is_file()]

    async def delete(self, file_id: str) -> bool:
        if not file_id:
            return False

        file_path = self.storage_path / file_id
        if not file_path.exists():
            return False

        file_path.unlink()
        return True

    def _guess_content_type(self, file_path: Path) -> str:
        extension = file_path.suffix.lower()
        if extension in (".jpg", ".jpeg"):
            return "image/jpeg"
        elif extension == ".png":
            return "image/png"
        elif extension == ".pdf":
            return "application/pdf"
        elif extension == ".mp4":
            return "video/mp4"
        return "application/octet-stream"
