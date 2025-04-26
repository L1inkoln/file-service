from abc import ABC, abstractmethod
from typing import AsyncGenerator, Tuple
from fastapi import UploadFile


class BaseStorage(ABC):
    @abstractmethod
    async def save(self, file: UploadFile) -> str:
        """Сохраняет файл и возвращает его идентификатор/путь"""
        pass

    @abstractmethod
    async def get(self, file_id: str) -> Tuple[AsyncGenerator[bytes, None], str, int]:
        """
        Возвращает:
        - генератор для чтения файла по частям
        - content_type
        - размер файла в байтах
        """
        pass

    @abstractmethod
    async def list(self) -> list[str]:
        """Список всех файлов"""
        pass

    @abstractmethod
    async def delete(self, file_id: str) -> bool:
        """Удаляет файл, возвращает bool значение об успешности"""
        pass
