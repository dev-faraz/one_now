# 1Now backend api

- What 1Now does: Provide SaaS backend for independent car rental operators, powering booking, fleet, and payments.

- Who it serves: Small operators (e.g., LahoreCarRental.com) needing an online customer-facing portal plus management dashboard.

Frontend integration: RESTful JSON endpoints consumed by React/Vue frontend; JWT tokens in headers; drivers for listing vehicles, creating bookings, user sessions.

## Setup

1. Clone repo: `git clone https://github.com/dev-faraz/one_now.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`


## API Documentation

## Authentication
- **POST /register**
  - Request: `{"username": "user1", "password": "pass123"}`
  - Response: `{"message": "User created successfully."}` (201)

- **POST /login**
  - Request: `{"username": "user1", "password": "pass123"}`
  - Response: `{"access": "<token>", "refresh": "<token>"}` (200)

## Vehicle Management
- **POST /vehicles/**
  - Request: `{"make": "Toyota", "model": "Corolla", "year": 2020, "plate": "ABC123"}`
  - Response: `{"id.": 1, "make": "Toyota", ...}` (201)

- **GET /vehicles/**
  - Response: `[ {"id": 1, "make": "Toyota", ...}, ... ]` (200)
