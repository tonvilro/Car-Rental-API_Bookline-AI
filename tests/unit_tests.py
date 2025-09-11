"""
Simple unit tests for controllers - testing business logic only
"""
from datetime import date
from unittest.mock import Mock
from app.controllers.car_controller import CarController
from app.controllers.booking_controller import BookingController
from app.models.car import Car
from app.models.booking import Booking


## GET AVAILABLE CARS UNIT TESTS

def test_car_controller_filters_available_cars():
    """Car Controller returns only available cars"""
    controller = CarController()

    # Mock data service
    mock_cars = [
        Car(id="car_001", brand="Porsche", model="GT3", year=2023, daily_price=450.0, 
            available=True, plate="ABC123", color="White", kilometers=1000),
        Car(id="car_002", brand="Audi", model="RS6", year=2022, daily_price=380.0,
            available=False, plate="DEF456", color="Black", kilometers=2000) # Not available
    ]
    controller.data_service.get_all_cars = Mock(return_value=mock_cars)
    controller.data_service.get_all_bookings = Mock(return_value=[])
    
    # Test
    result = controller.get_available_cars()
    
    # Only available car should be returned
    assert len(result) == 1
    assert result[0].id == "car_001"
    assert result[0].brand == "Porsche"


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
    exception_raised = False
    exception_message = ""
    try:
        controller.create_booking(
            car_id="invalid",
            customer_name="Ton Vilà", 
            customer_email="ton@vila.com",
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 3)
        )
    except ValueError as e:
        exception_raised = True
        exception_message = str(e)
    
    assert exception_raised
    assert "not found" in exception_message


def test_booking_controller_calculates_price():
    """Booking Controller calculates total price correctly"""
    controller = BookingController()
    
    # Mock car (daily price 380)
    mock_car = Car(id="car_003", brand="Audi", model="RS6", year=2022, daily_price=380.0,
                   available=True, plate="XYZ789", color="Silver", kilometers=15000)
    
    controller.data_service.get_all_cars = Mock(return_value=[mock_car])
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
    exception_raised = False
    exception_message = ""
    try:
        controller.create_booking(
            car_id="car_001",
            customer_name="Test Customer",
            customer_email="test@test.com",
            start_date=date(2025, 9, 1),  # Past date
            end_date=date(2025, 9, 3)
        )
    except ValueError as e:
        exception_raised = True
        exception_message = str(e)
    
    assert exception_raised
    assert "past" in exception_message


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
    exception_raised = False
    exception_message = ""
    try:
        controller.create_booking(
            car_id="car_001",
            customer_name="Test Customer",
            customer_email="test@test.com",
            start_date=date(2025, 12, 12),  # Overlaps existing booking
            end_date=date(2025, 12, 17)
        )
    except ValueError as e:
        exception_raised = True
        exception_message = str(e)
    
    assert exception_raised
    assert "already booked" in exception_message
    assert "2025-12-10" in exception_message  # Should show existing booking dates
    assert "2025-12-15" in exception_message