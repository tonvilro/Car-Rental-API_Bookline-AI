from typing import List
from datetime import datetime, date
from app.models.data_service import DataService
from app.models.car import Car
from app.models.booking import Booking
import logging
import uuid

logger = logging.getLogger(__name__)


class BookingController:
    def __init__(self):
        self.data_service = DataService()
    
    def create_booking(self, car_id: str, customer_name: str, customer_email: str, 
                      start_date: date, end_date: date) -> Booking:
        """
        Create a new booking for a car
        """
        # Get car to calculate price
        cars = self.data_service.get_all_cars()
        car = next((c for c in cars if c.id == car_id), None)
        
        # Car not found
        if not car:
            raise ValueError(f"Car {car_id} not found")

        # Car not available
        if not car.available:
            raise ValueError(f"Car {car_id} is not available")
        
        # Check for date conflicts with existing bookings
        bookings = self.data_service.get_all_bookings()
        for existing_booking in bookings:
            if (existing_booking.car_id == car_id and 
                existing_booking.status == "confirmed"):
                existing_start = existing_booking.start_date.date()
                existing_end = existing_booking.end_date.date()
                
                # Check date overlap: new booking overlaps if start <= existing_end and end >= existing_start
                if (start_date <= existing_end and end_date >= existing_start):
                    raise ValueError(f"Car {car_id} is already booked from {existing_start} to {existing_end}")
        
        # Validate dates
        if start_date < date.today():
            raise ValueError("Cannot book dates in the past")
        
        # Calculate total price
        duration_days = (end_date - start_date).days
        if duration_days <= 0:
            raise ValueError("End date must be after start date")
        
        total_price = duration_days * car.daily_price

        booking_id = "BOOKING-" + str(uuid.uuid4())
        
        # Create booking
        booking = Booking(
            id=booking_id,
            car_id=car_id,
            customer_name=customer_name,
            customer_email=customer_email,
            start_date=datetime.combine(start_date, datetime.min.time()),
            end_date=datetime.combine(end_date, datetime.min.time()),
            total_price=total_price
        )
        
        # Save
        success = self.data_service.create_booking(booking)
        if not success:
            raise ValueError("Failed to create booking")
        
        return booking
