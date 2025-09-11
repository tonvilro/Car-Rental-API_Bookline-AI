import os
import logging
from fastapi import FastAPI
from app.views.car_views import router as car_router

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = FastAPI(title="Car Rental API", version="1.0.0")

app.include_router(car_router)

@app.get("/")
async def root():
    return {"Welcome to the Car Rental API"}

@app.get("/data-path")
async def data_path():
    data_path = os.getenv("DATA_PATH", "data")
    logger.info(f"Data path is set to: {data_path}")
    return {"data_path": data_path}