# 📁 File Service
>[!NOTE]
>File Service — это лёгкий асинхронный сервис на FastAPI для загрузки, скачивания, просмотра и удаления файлов.  
Файлы сохраняются локально на диск в папке с репозиторием(можно указать любой путь в config). Подключить s3 хранилище можно реализовав абстракцию base и настроив config s3. Реализовано с разделением логики на слои 
(API → Service → Storage).

## 🚀 Стек технологий

-  FastAPI — фреймворк для создания API
-  aiofiles — асинхронная работа с файлами
-  Poetry — управление зависимостями
- Python 3.13

## 🏗 Архитектура проекта
FastAPI Router (files.py)

        ↓
Service Layer (file_service.py)

        ↓
Storage Layer (local.py)

        ↓
Файловая система

---

*Чистое разделение на API, Service и Storage уровни*

*Асинхронная работа с файлами через aiofiles*

*Поддержка больших файлов через стриминг*

## 📦 Установка проекта

1. Клонируйте репозиторий:

```
git clone https://github.com/L1inkoln/file-service.git
cd file-service
```
Установите зависимости через Poetry и запустите приложение:
```
poetry install
poetry run uvicorn app.main:app
```
После запуска информация об API будет доступна по адресу:

- http://localhost:8000

Документация Swagger UI:

- http://localhost:8000/docs
## ✨ Возможности API
### 📥 Загрузка одного файла
POST /files/

*Параметры:*

файл для загрузки (формат multipart/form-data)

### 📥 Загрузка нескольких файлов
POST /files/multiple/

*Параметры:*

files: список файлов для загрузки

### 📃 Получить список всех файлов
GET /files/

### 📥 Скачать файл
GET /files/{filename}

### ❌ Удалить файл
DELETE /files/{filename}