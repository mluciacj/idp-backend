from fastapi import FastAPI
from app.api.v1.endpoints.upload import router as upload_router
from app.api.v1.endpoints.documents import router as documents_router
from app.api.v1.endpoints.authorizations import router as authorizations_router
from app.api.v1.endpoints.session import router as session_router
from app.api.v1.endpoints.subscriptions import router as subscriptions_router
from app.api.v1.endpoints.billing import router as billing_router
from app.api.v1.endpoints.pageviews import router as pageviews_router
from app.api.v1.endpoints.funnel import router as funnel_router
from app.api.v1.endpoints.userevents import router as userevents_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(documents_router)
app.include_router(authorizations_router)
app.include_router(session_router)
app.include_router(subscriptions_router)
app.include_router(billing_router)
app.include_router(pageviews_router)
app.include_router(funnel_router)
app.include_router(userevents_router)
