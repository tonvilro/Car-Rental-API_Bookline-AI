from typing import List, Optional
from datetime import date, datetime
from app.models.data_service import DataService
from app.models.car import Car
from app.models.booking import Booking
import logging

logger = logging.getLogger(__name__)


class CarController:    
    def __init__(self):
        self.data_service = DataService()
    
    def get_available_cars(self, date: Optional[date] = None) -> List[Car]:
        """
        Get cars available for a date
        If no date provided, return all cars
        """
        logger.info(f"Querying available cars" + (f" for date {date}" if date else ""))
        cars = self.data_service.get_all_cars()
        logger.debug(f"Found {len(cars)} total cars")
        
        # If no date filter return all available cars
        if not date:
            available_cars = [car for car in cars if car.available]
            logger.info(f"No date provided. Returning {len(available_cars)} available cars")
            return available_cars
        
        # Filter by date
        bookings = self.data_service.get_all_bookings()
        logger.debug(f"Found {len(bookings)} bookings")
        available_cars = []
        
        for car in cars:
            if not car.available:
                logger.debug(f"Car {car.id} is unavailable, skipping")
                continue
                
            # Check if car is booked on target date
            is_booked = False
            for booking in bookings:
                if booking.car_id == car.id and booking.status == "confirmed":
                    booking_start = booking.start_date.date()
                    booking_end = booking.end_date.date()
                    
                    # Check if target date overlaps with booking
                    if booking_start <= date <= booking_end:
                        logger.debug(f"Car {car.id} is booked from {booking_start} to {booking_end}, conflicts with {date}")
                        is_booked = True
                        break
            
            if not is_booked:
                available_cars.append(car)
                
        logger.info(f"Found {len(available_cars)} cars available for {date}")
        return available_cars
