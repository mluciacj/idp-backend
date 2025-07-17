from fastapi import FastAPI
from app.api.v1.endpoints.upload import router as upload_router

app = FastAPI()

app.include_router(upload_router)
