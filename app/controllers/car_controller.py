from typing import List
from app.models.data_service import DataService
from app.models.car import Car
import logging

logger = logging.getLogger(__name__)

class CarController:    
    def __init__(self):
        self.data_service = DataService()
    
    def get_available_cars(self) -> List[Car]:
        cars = self.data_service.get_all_cars()
        return cars
