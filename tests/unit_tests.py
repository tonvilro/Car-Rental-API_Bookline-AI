"""
Simple unit tests for controllers - testing business logic only
"""
import pytest
from datetime import date
from unittest.mock import Mock
from app.controllers.car_controller import CarController
from app.controllers.booking_controller import BookingController
from app.models.car import Car
from app.models.booking import Booking


@pytest.fixture
def sample_cars():
    """Sample cars"""
    return [
        Car(id="car_001", brand="Porsche", model="GT3", year=2023, daily_price=450.0,
            available=True, plate="ABC123", color="White", kilometers=1000),
        Car(id="car_002", brand="Audi", model="RS6", year=2022, daily_price=380.0,
            available=False, plate="DEF456", color="Black", kilometers=2000),
        Car(id="car_003", brand="Audi", model="RS6", year=2022, daily_price=380.0,
            available=True, plate="XYZ789", color="Silver", kilometers=15000)
    ]


@pytest.fixture
def sample_booking():
    """Sample booking"""
    return Mock(
        car_id="car_001", 
        status="confirmed",
        start_date=Mock(date=Mock(return_value=date(2025, 12, 10))),
        end_date=Mock(date=Mock(return_value=date(2025, 12, 15)))
    )


## GET AVAILABLE CARS UNIT TESTS

def test_car_controller_filters_available_cars(sample_cars):
    """Car Controller returns only available cars"""
    controller = CarController()

    # Mock data service
    controller.data_service.get_all_cars = Mock(return_value=sample_cars)
    controller.data_service.get_all_bookings = Mock(return_value=[])
    
    # Test
    result = controller.get_available_cars()
    
    # Only available cars should be returned (car_001 and car_003)
    assert len(result) == 2
    available_ids = {car.id for car in result}
    assert available_ids == {"car_001", "car_003"}
    assert all(car.available for car in result)


def test_car_controller_date_filtering():
    """Car Controller filters by booking dates"""
    controller = CarController()
    
    # Mock cars
    mock_cars = [
        Car(id="car_001", brand="Porsche", model="GT3", year=2023, daily_price=450.0,
            available=True, plate="ABC123", color="White", kilometers=1000),
        Car(id="car_002", brand="Audi", model="RS6", year=2022, daily_price=380.0,
            available=True, plate="DEF456", color="Black", kilometers=2000)
    ]
    
    # car_001 booked from 2025-12-01 to 2025-12-05
    mock_bookings = [
        Mock(car_id="car_001", status="confirmed", 
             start_date=Mock(date=Mock(return_value=date(2025, 12, 1))),
             end_date=Mock(date=Mock(return_value=date(2025, 12, 5))))
    ]
    
    controller.data_service.get_all_cars = Mock(return_value=mock_cars)
    controller.data_service.get_all_bookings = Mock(return_value=mock_bookings)
    
    # Test date during booking
    result = controller.get_available_cars(date(2025, 12, 3))
    
    # Only car_002 should be available
    assert len(result) == 1
    assert result[0].id == "car_002"


## BOOKING UNIT TESTS

def test_booking_controller_validates_car_exists():
    """Booking Controller validates car exists"""
    controller = BookingController()
    
    # Mock empty cars list
    controller.data_service.get_all_cars = Mock(return_value=[])
    
    # Test booking invalid car
    with pytest.raises(ValueError, match="not found"):
        controller.create_booking(
            car_id="invalid",
            customer_name="Ton Vilà", 
            customer_email="ton@vila.com",
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 3)
        )


def test_booking_controller_calculates_price(sample_cars):
    """Booking Controller calculates total price correctly"""
    controller = BookingController()
    
    # Use car_003 (daily price 380)
    controller.data_service.get_all_cars = Mock(return_value=sample_cars)
    controller.data_service.get_all_bookings = Mock(return_value=[])
    controller.data_service.create_booking = Mock(return_value=True)
    
    # Test 3-day booking
    result = controller.create_booking(
        car_id="car_003",
        customer_name="Ton Vilà",
        customer_email="ton@vila.com", 
        start_date=date(2025, 12, 1),
        end_date=date(2025, 12, 4)  # 3 days
    )
    
    # Should calculate: 3 days × 380 = 1140
    assert result.total_price == 1140.0
    assert result.car_id == "car_003"
    assert result.status == "confirmed"


def test_booking_controller_prevents_past_dates():
    """Booking Controller prevents past date bookings"""
    controller = BookingController()
    
    # Mock available car
    mock_car = Car(id="car_001", brand="Porsche", model="GT3", year=2023, daily_price=450.0,
                   available=True, plate="ABC123", color="White", kilometers=1000)
    
    controller.data_service.get_all_cars = Mock(return_value=[mock_car])
    controller.data_service.get_all_bookings = Mock(return_value=[])
    
    # Test past date booking
    with pytest.raises(ValueError, match="past"):
        controller.create_booking(
            car_id="car_001",
            customer_name="Test Customer",
            customer_email="test@test.com",
            start_date=date(2025, 9, 1),  # Past date
            end_date=date(2025, 9, 3)
        )


def test_booking_controller_detects_overlapping_dates():
    """Booking Controller detects overlapping bookings"""
    controller = BookingController()
    
    # Mock available car
    mock_car = Car(id="car_001", brand="Porsche", model="GT3", year=2023, daily_price=450.0,
                   available=True, plate="ABC123", color="White", kilometers=1000)
    
    # Mock existing booking: Dec 10-15, 2025
    existing_booking = Mock(
        car_id="car_001", 
        status="confirmed",
        start_date=Mock(date=Mock(return_value=date(2025, 12, 10))),
        end_date=Mock(date=Mock(return_value=date(2025, 12, 15)))
    )
    
    controller.data_service.get_all_cars = Mock(return_value=[mock_car])
    controller.data_service.get_all_bookings = Mock(return_value=[existing_booking])
    
    # Test overlapping booking: Dec 12-17 (overlaps with Dec 10-15)
    with pytest.raises(ValueError, match="already booked.*2025-12-10.*2025-12-15"):
        controller.create_booking(
            car_id="car_001",
            customer_name="Test Customer",
            customer_email="test@test.com",
            start_date=date(2025, 12, 12),  # Overlaps existing booking
            end_date=date(2025, 12, 17)
        )