from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    storage_path: str = "./storage"
    storage_type: str = "local"  # можно добавить s3

    class Config:
        env_file = ".env"


settings = Settings()
