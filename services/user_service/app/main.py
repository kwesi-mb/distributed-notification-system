from fastapi import FastAPI, Depends 

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.dependencies.database import get_db 

from app.core.config import settings
from app.core.logger import logger 
from app.api.v1.users import router as user_router

logger.info("Starting User Service...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

@app.get("/")
async def root():
    return {
        "success": True,
        "message": f"{settings.APP_NAME} is running."
    }

@app.get("/health")
async def health(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))


    return {
        "success": True,
        "message": f"{settings.APP_NAME} is healthy.",
        "data": {
            "status": "healthy",
            "environment": settings.ENVIRONMENT
        },
    }

app.include_router(
    user_router,
    prefix="/api/v1",
)