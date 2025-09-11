from fastapi import APIRouter, HTTPException
from datetime import date
from app.models.booking import Booking
from app.controllers.booking_controller import BookingController
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookings", tags=["bookings"])
booking_controller = BookingController()


class BookingRequest(BaseModel):
    car_id: str
    customer_name: str
    customer_email: str
    start_date: date
    end_date: date


@router.post("/", response_model=Booking)
async def create_booking(booking_request: BookingRequest):
    """
    Create a new car booking
    """
    try:
        booking = booking_controller.create_booking(
            car_id=booking_request.car_id,
            customer_name=booking_request.customer_name,
            customer_email=booking_request.customer_email,
            start_date=booking_request.start_date,
            end_date=booking_request.end_date
        )
        logger.info(f"Booking created successfully: {booking.id}")
        return booking
    
    except ValueError as e:
        logger.error(f"Booking validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except RuntimeError as e:
        logger.error(f"Booking creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
