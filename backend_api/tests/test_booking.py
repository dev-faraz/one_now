from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ..models import Vehicle, Booking
from ..serializers import VehicleSerializer
from django.contrib.auth.models import User
from rest_framework import status
from django.utils.http import urlencode
from datetime import date
from dateutil.parser import isoparse


class BookingViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_bookings(self):
        """Test that only bookings for the user's vehicles are listed."""
        user = User.objects.create_user(username='testuser', password='testpass')
        vehicle = Vehicle.objects.create(user=user, make='Toyota', model='Corolla', year=2020, plate="KBC-215")
        Booking.objects.create(vehicle=vehicle, start_date='2026-01-01', end_date='2026-01-05')
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_vehicle = Vehicle.objects.create(user=other_user, make='Ford', model='Focus', year=2018, plate="POL-394")
        Booking.objects.create(vehicle=other_vehicle, start_date='2026-01-01', end_date='2026-01-05')
        vehicle_json =  VehicleSerializer(vehicle).data

        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['vehicle'], vehicle_json)

    def test_create_booking_with_own_vehicle(self):
        """Test creating a booking for the user's own vehicle."""
        user = User.objects.create_user(username='testuser', password='testpass')
        vehicle = Vehicle.objects.create(user=user, make='Toyota', model='Corolla', year=2020, plate="ACW-7576")
        self.client.force_authenticate(user=user)
        data = {'vehicle': vehicle.pk, 'start_date': '2026-01-01', 'end_date': '2026-01-05'}
        response = self.client.post(reverse('booking-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.get(vehicle=vehicle)
        self.assertEqual(booking.start_date.strftime('%Y-%m-%d'), '2026-01-01')

    def test_create_booking_with_other_user_vehicle(self):
        """Test that booking another user's vehicle raises PermissionDenied."""
        user = User.objects.create_user(username='testuser', password='testpass')
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_vehicle = Vehicle.objects.create(user=other_user, make='Ford', model='Focus', year=2018, plate="AHR-2960")
        self.client.force_authenticate(user=user)
        data = {'vehicle': other_vehicle.pk, 'start_date': '2026-01-01', 'end_date': '2026-01-05'}
        response = self.client.post(reverse('booking-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You can only book your own vehicles.')

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access the endpoint."""
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_bookings_with_date_filter(self):
        """Test filtering bookings by ?from= and ?to= query params."""
        user = User.objects.create_user(username='testuser', password='testpass')
        vehicle = Vehicle.objects.create(user=user, make='Honda', model='Civic', year=2022, plate="ABC-123")

        Booking.objects.create(vehicle=vehicle, start_date='2026-01-01', end_date='2026-01-05')
        Booking.objects.create(vehicle=vehicle, start_date='2026-03-01', end_date='2026-03-05')

        self.client.force_authenticate(user=user)
        query = urlencode({'from': '2026-01-01', 'to': '2026-01-31'})
        url = f"{reverse('booking-list')}?{query}"
        response = self.client.get(url)
        parsed_date = isoparse(response.data[0]['start_date']).date()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(parsed_date, date(2026, 1, 1))
