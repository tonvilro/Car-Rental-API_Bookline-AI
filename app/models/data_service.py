import json
import os
from typing import List
from app.models.car import Car
from app.models.booking import Booking
import logging

logger = logging.getLogger(__name__)

class DataService:
    """
    Intermediary for reading and writing to the JSON files.
    """
    
    def __init__(self, data_path: str = None):
        self.data_path = data_path or os.getenv("DATA_PATH", "data")
        self.cars_file = os.path.join(self.data_path, "cars.json")
        self.bookings_file = os.path.join(self.data_path, "bookings.json")
        self.setup_files()
    
    def setup_files(self):
        """Make sure the data folder and files exist"""
        os.makedirs(self.data_path, exist_ok=True)
        
        if not os.path.exists(self.cars_file):
            with open(self.cars_file, 'w') as f:
                json.dump([], f)
                
        if not os.path.exists(self.bookings_file):
            with open(self.bookings_file, 'w') as f:
                json.dump([], f)
    
    def get_all_cars(self) -> List[Car]:
        """Read all cars from the JSON file"""
        try:
            with open(self.cars_file, 'r') as f:
                cars_data = json.load(f)
            
            # Convert each dictionary to a Car object
            cars = []
            for car_dict in cars_data:
                car = Car(**car_dict)
                cars.append(car)
            
            return cars
        
        except Exception as e:
            logger.error(f"Could not load cars: {e}")
            return []
    
    def get_all_bookings(self) -> List[Booking]:
        """Read all bookings from the JSON file"""
        try:
            with open(self.bookings_file, 'r') as f:
                bookings_data = json.load(f)
            
            # Convert each dictionary to a Booking object
            bookings = []
            for booking_dict in bookings_data:
                booking = Booking(**booking_dict)
                bookings.append(booking)
            
            return bookings
        
        except Exception as e:
            logger.error(f"Could not load bookings: {e}")
            return []
    
    def create_booking(self, booking: Booking) -> bool:
        """Add a new booking to the JSON file"""
        try:
            # Read current bookings
            with open(self.bookings_file, 'r') as f:
                bookings_data = json.load(f)
            
            # Add the new booking
            bookings_data.append(booking.dict())
            
            # Write everything back to the file
            with open(self.bookings_file, 'w') as f:
                json.dump(bookings_data, f, indent=2, default=str)
            
            logger.info(f"Created booking {booking.id} for car {booking.car_id}")
            return True
        
        except Exception as e:
            logger.error(f"Could not create booking: {e}")
            return False
