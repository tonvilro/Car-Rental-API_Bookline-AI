from fastapi import APIRouter
from typing import List
from app.models.car import Car
from app.controllers.car_controller import CarController
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cars", tags=["cars"])
car_controller = CarController()

@router.get("/available", response_model=List[Car])
async def get_available_cars():
    cars = car_controller.get_available_cars()
    logger.info(f"Available cars: {len(cars)} cars")
    return cars