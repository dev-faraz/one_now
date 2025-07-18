# 1Now backend api

- # What 1Now Does
    - 1Now builds digital tools that help small and independent car rental companies manage their daily operations. These tools include online booking systems, vehicle fleet management, rental agreements, calendar views, and payment integration — effectively modernizing car rental businesses with cloud-based solutions.

- # Who 1Now Serves
    - 1Now primarily serves small to mid-sized local rental agencies, such as LahoreCarRental.com, who often lack the resources to build and maintain custom tech stacks. These operators need simple, reliable backend systems to support their operations and customer bookings.

- # How This Backend Connects to LahoreCarRental.com Frontend
    - his Django REST API serves as the backend engine powering LahoreCarRental.com. The frontend, which could be built in any modern JavaScript framework (e.g., React, Vue, Angular), will connect to this backend through HTTP requests to the exposed REST endpoints.

## Setup

1. Clone repo: `git clone https://github.com/dev-faraz/one_now.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`


## API Documentation


# POST /register/
 - Description: Registers a new user.
 - Request: {"username": "user1", "password": "pass123"}
 - Response:
    - Success: {"message": "User created successfully."} (201)
    - Error: {"error": "Username and password are required."} (400) or {"error": "Username already exists."} (400)

# POST /login/
  - Description: Authenticates a user and returns access and refresh tokens.
  - Request: {"username": "user1", "password": "pass123"}
  - Response: {"access": "<token>", "refresh": "<token>"} (200)

# Vehicle Management POST /vehicles/
  - Description: Creates a new vehicle for the authenticated user.
  - Authentication: Requires JWT token in the Authorization header.
  - Request: {"make": "Toyota", "model": "Corolla", "year": 2020, "plate": "ABC123"}
  - Response: {"id": 1, "make": "Toyota", "model": "Corolla", "year": 2020, "plate": "ABC123", "user": "<username>"} (201)

# GET /vehicles/
  - Description: Retrieves a list of vehicles owned by the authenticated user.
  - Authentication: Requires JWT token in the Authorization header.
  - Response: [ {"id": 1, "make": "Toyota", "model": "Corolla", "year": 2020, "plate": "ABC123", "user": "<username>"}, ... ] (200)

# GET /vehicles/{id}/
  - Description: Retrieves details of a specific vehicle owned by the authenticated user.
  - Authentication: Requires JWT token in the Authorization header.
  - Response: {"id": 1, "make": "Toyota", "model": "Corolla", "year": 2020, "plate": "ABC123", "user": "<username>"} (200)

# PUT /vehicles/{id}/
  - Description: Updates a specific vehicle owned by the authenticated user.
  - Authentication: Requires JWT token in the Authorization header.
  - Request: {"make": "Toyota", "model": "Camry", "year": 2021, "plate": "XYZ789"}
  - Response: {"id": 1, "make": "Toyota", "model": "Camry", "year": 2021, "plate": "XYZ789", "user": "<username>"} (200)

# DELETE /vehicles/{id}/
  - Description: Deletes a specific vehicle owned by the authenticated user.
  - Authentication: Requires JWT token in the Authorization header.
  - Response: No content (204)

# Booking ManagementPOST /bookings/
  - Description: Creates a new booking for a vehicle owned by the authenticated user.
  - Authentication: Requires JWT token in the Authorization header.
  - Request: {"vehicle": 1, "start_date": "2025-07-20", "end_date": "2025-07-25"}
  - Response: {"id": 1, "vehicle": 1, "start_date": "2025-07-20", "end_date": "2025-07-25"} (201)
  - Error: {"detail": "You can only book your own vehicles."} (403)

# GET /bookings/
  - Description: Retrieves a list of bookings for vehicles owned by the authenticated user, optionally filtered by date range.
  - Authentication: Requires JWT token in the Authorization header.
  - Query Parameters:
    - from: Filter bookings with start date greater than or equal to this date (e.g., 2025-07-20).
    - to: Filter bookings with end date less than or equal to this date (e.g., 2025-07-25).
  - Response: [ {"id": 1, "vehicle": 1, "start_date": "2025-07-20", "end_date": "2025-07-25"}, ... ] (200)

# GET /bookings/{id}/
  - Description: Retrieves details of a specific booking for a vehicle owned by the authenticated user.
  - Authentication: Requires JWT token in the Authorization header.
  - Response: {"id": 1, "vehicle": 1, "start_date": "2025-07-20", "end_date": "2025-07-25"} (200)

# PUT /bookings/{id}/
  - Description: Updates a specific booking for a vehicle owned by the authenticated user.
  - Authentication: Requires JWT token in the Authorization header.
  - Request: {"vehicle": 1, "start_date": "2025-07-21", "end_date": "2025-07-26"}
  - Response:
    - {"id": 1, "vehicle": 1, "start_date": "2025-07-21", "end_date": "2025-07-26"} (200)
    - Error: {"detail": "You can only book your own vehicles."} (403)

# DELETE /bookings/{id}/
  - Description: Deletes a specific booking for a vehicle owned by the authenticated user.
  - Authentication: Requires JWT token in the Authorization header.
  - Response: No content (204)


