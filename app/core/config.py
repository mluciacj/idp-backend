from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    S3_ENDPOINT: str
    S3_BUCKET_NAME: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION: str
    POSTGRES_URL: str
    GOOGLE_GENAI_API_KEY: str
    OPENAI_API_KEY: str
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
