from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Car(BaseModel):
    """
    Represents an individual car unit in the rental fleet.
    Each car is a unique vehicle with its own availability status.
    Each car can be associated with multiple bookings.
    """
    id: str = Field(...)
    brand: str = Field(...)
    model: str = Field(...)
    year: int = Field(..., ge=1900, le=2030)
    daily_price: float = Field(..., gt=0)
    available: bool = Field(default=True)
    plate: str = Field(...)
    color: str = Field(...)
    kilometers: int = Field(..., ge=0)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
