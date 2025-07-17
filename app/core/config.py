from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    S3_ENDPOINT: str
    S3_BUCKET_NAME: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION: str
    POSTGRES_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
