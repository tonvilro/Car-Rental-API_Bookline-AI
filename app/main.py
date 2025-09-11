import os
import logging
from fastapi import FastAPI
from app.views.car_views import router as car_router
from app.views.booking_views import router as booking_router

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = FastAPI(title="Car Rental API", version="1.0.0")

app.include_router(car_router)
app.include_router(booking_router)

@app.get("/")
async def root():
    return {"Welcome to the Car Rental API"}