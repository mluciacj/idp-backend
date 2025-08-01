from fastapi import FastAPI
from app.api.v1.endpoints.upload import router as upload_router
from app.api.v1.endpoints.documents import router as documents_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(documents_router)
