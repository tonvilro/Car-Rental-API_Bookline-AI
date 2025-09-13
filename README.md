# Car Rental API

API for managing car rentals built with FastAPI

## Endpoints

### GET /cars/available
Lists all available cars, filtered by date (optional).

**Query Parameters:**
- `date` (optional): Filter cars available on this specific date (YYYY-MM-DD format)

### POST /bookings/
Creates a new car booking.

**Request Body:**
```json
{
  "car_id": "car_001",
  "customer_name": "Ton Vilà",
  "customer_email": "ton@vila.com",
  "start_date": "2025-12-01",
  "end_date": "2025-12-05"
}
```

## Architecture

The application follows a layered based approach. MVC. It keeps it all separated and modular.

- **Models**: Contains the  models definitions
- **Views**: Contains the endpoint definitions + validation 
- **Controllers**: Logic layer with all the operation
- **Data Service**: Intermediary layer to access the JSON data in files

### Other Design Decisions
- **Pydantic Models**: Helps with data validation and model definition
- **Pytest**: Helps with easy unit testing
- **Docker Compose**: For now the API data is stored in JSON files but in the future if it is stored in a DB it will be very easy to add to the system. We will need to make some changes in the data service as it will now be accessing a DB. We could use the SQLAlchemy library to do so along with Alembic for the migrations.

### Requisite Decisions
- **Booking Status**: New bookings are created with "confirmed" status by default. In the future this could include states like cancelled, pending payment, finished, customer didn't show up...
- **Is Car Avilable**: Car must be marked as available true and not have conflicting bookings
- **Date Validation**: No bookings allowed for past dates. Must be >= today
- **Booking IDs**: Booking IDs use format: "BOOKING-{uuid}"

## How to Run

### Prerequisites
- Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/tonvilro/Bookline-AI.git
   cd Bookline-AI
   ```

2. **Create environment file**
   ```bash
   cp sample.env .env
   ```

3. **Start the application**
   ```bash
   docker compose up --build -d
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Docs 1: http://localhost:8000/docs
   - Docs 2: http://localhost:8000/redoc

## Sample Data

The repository includes 3 vehicle JSON data for easy testing. This way the user can test it directly not having to manually create vehicles. Bookings are empty.

## Run Tests

```bash
# Make sure container is running first
docker compose up -d

# Run tests
docker exec bookline-ai-car_rental_api-1 python -m pytest tests/unit_tests.py -v
```

## Example Calls

### 1. List Available Cars
```bash
curl "http://localhost:8000/cars/available"
```

### 2. List Cars Available on Specific Date
```bash
curl "http://localhost:8000/cars/available?date=2025-12-01"
```

### 3. Create a Booking
```bash
curl -X POST "http://localhost:8000/bookings/" \
  -H "Content-Type: application/json" \
  -d '{
    "car_id": "car_001",
    "customer_name": "Ton Vilà", 
    "customer_email": "ton@vila.com",
    "start_date": "2025-12-01",
    "end_date": "2025-12-05"
  }'
```
