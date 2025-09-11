from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Booking(BaseModel):
    """
    Represents a car rental booking.
    Links a customer to a specific car for a date range.
    A booking only can be associated with one car.
    """
    id: str = Field(...)
    car_id: str = Field(...)
    customer_name: str = Field(..., min_length=1)
    customer_email: str = Field(...)
    start_date: datetime = Field(...)
    end_date: datetime = Field(...)
    status: str = Field(default="confirmed")
    total_price: float = Field(..., gt=0)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
