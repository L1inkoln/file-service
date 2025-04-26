from functools import wraps
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Annotated, List
from app.services.file_service import FileService
from app.schemas.files import (
    FileUploadResponse,
    MultipleFileUploadResponse,
    FileDeleteResponse,
    FilesListResponse,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/files",
    tags=["files"],
)

# Инициализация сервиса
service = FileService()


# Декоратор для единой обработки ошибок
def handle_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Unhandled error")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    return wrapper


@router.post(
    "/",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a single file",
    response_description="Filename of the uploaded file",
)
@handle_errors
async def upload_file(file: Annotated[UploadFile, File(...)]):
    """
    Upload a single file to the server.

    - **file**: The file to upload (required)
    - **Returns**: Filename and success message
    """
    # Сохраняем файл через сервис
    filename = await service.upload_file(file)
    logger.info(f"Uploaded file: {filename}")
    return FileUploadResponse(filename=filename)


@router.post(
    "/multiple/",
    response_model=MultipleFileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload multiple files",
    response_description="List of uploaded filenames",
)
@handle_errors
async def upload_multiple_files(files: Annotated[List[UploadFile], File(...)]):
    """
    Upload multiple files to the server.

    - **files**: List of files to upload (required)
    - **Returns**: List of uploaded filenames and success message
    """
    filenames = []
    for file in files:
        filename = await service.upload_file(file)
        filenames.append(filename)
        logger.info(f"Uploaded file: {filename}")

    return MultipleFileUploadResponse(filenames=filenames, count=len(filenames))


@router.get(
    "/",
    response_model=FilesListResponse,
    summary="List all files",
    response_description="List of available filenames",
)
@handle_errors
async def list_files():
    """
    Get a list of all available files.

    - **Returns**: List of filenames
    """
    files = await service.list_files()
    logger.info(f"Listed files: {files}")
    return FilesListResponse(files=files)


@router.get(
    "/{filename}",
    summary="Download a file",
    response_description="File content stream",
)
@handle_errors
async def download_file(filename: str):
    """
    Download a file by its filename.

    - **filename**: Name of the file to download (required)
    - **Returns**: StreamingResponse with file content
    """
    file_gen, content_type, file_size = await service.download_file(filename)
    logger.info(f"Downloaded file: {filename} ({file_size} bytes)")
    return StreamingResponse(
        content=file_gen,
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(file_size),
            "Accept-Ranges": "bytes",
        },
    )


@router.delete(
    "/{filename}",
    response_model=FileDeleteResponse,
    summary="Delete a file",
    response_description="Deletion status",
)
@handle_errors
async def delete_file(filename: str):
    """
    Delete a file by its filename.

    - **filename**: Name of the file to delete (required)
    - **Returns**: Deletion status
    """
    success = await service.delete_file(filename)
    if not success:
        logger.warning(f"File not found for deletion: {filename}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    logger.info(f"Deleted file: {filename}")
    return FileDeleteResponse(filename=filename)
