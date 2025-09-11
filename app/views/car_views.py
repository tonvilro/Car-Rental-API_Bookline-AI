from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import date
from app.models.car import Car
from app.controllers.car_controller import CarController
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cars", tags=["cars"])
car_controller = CarController()


@router.get("/available", response_model=List[Car])
async def get_available_cars(date: Optional[date] = Query(None, description="Filter cars available on this date")):
    """
    Get available cars, optionally filtered by date
    """
    cars = car_controller.get_available_cars(date=date)
    logger.info(f"Available cars on {date}: {len(cars)} cars")
    return cars