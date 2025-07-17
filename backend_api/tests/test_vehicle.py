from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ..models import Vehicle
from django.contrib.auth.models import User
from rest_framework import status

class VehicleViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_vehicles(self):
        """Test that only the authenticated user's vehicles are listed."""
        user = User.objects.create_user(username='testuser', password='testpass')
        Vehicle.objects.create(user=user, make='Toyota', model='Corolla', year=2020, plate="ABC-123")
        Vehicle.objects.create(user=user, make='Honda', model='Civic', year=2019, plate="ABC-124")
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        Vehicle.objects.create(user=other_user, make='Ford', model='Focus', year=2018, plate="ABC-225")

        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('vehicle-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        vehicle_makes = [vehicle['make'] for vehicle in response.data]
        self.assertIn('Toyota', vehicle_makes)
        self.assertIn('Honda', vehicle_makes)
        self.assertNotIn('Ford', vehicle_makes)

    def test_create_vehicle(self):
        """Test that a vehicle is created and associated with the authenticated user."""
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        data = {'make': 'Tesla', 'model': 'Model S', 'year': 2021, 'plate': 'GHR-532'}
        response = self.client.post(reverse('vehicle-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vehicle = Vehicle.objects.get(make='Tesla')
        self.assertEqual(vehicle.user, user)

    def test_retrieve_vehicle(self):
        """Test retrieving a vehicle owned by the user and attempting to retrieve another user's vehicle."""
        user = User.objects.create_user(username='testuser', password='testpass')
        vehicle = Vehicle.objects.create(user=user, make='Toyota', model='Corolla', year=2020, plate="ABC-129")
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('vehicle-detail', kwargs={'pk': vehicle.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['make'], 'Toyota')

        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_vehicle = Vehicle.objects.create(user=other_user, make='Ford', model='Focus', year=2018, plate="ABC-144")
        response = self.client.get(reverse('vehicle-detail', kwargs={'pk': other_vehicle.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_vehicle(self):
        """Test updating a vehicle owned by the user."""
        user = User.objects.create_user(username='testuser', password='testpass')
        vehicle = Vehicle.objects.create(user=user, make='Toyota', model='Corolla', year=2020, plate="ABC-555")
        self.client.force_authenticate(user=user)
        data = {'make': 'Toyota', 'model': 'Camry', 'year': 2021, 'plate': 'GHR-532'}
        response = self.client.put(reverse('vehicle-detail', kwargs={'pk': vehicle.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.model, 'Camry')

    def test_delete_vehicle(self):
        """Test deleting a vehicle owned by the user."""
        user = User.objects.create_user(username='testuser', password='testpass')
        vehicle = Vehicle.objects.create(user=user, make='Toyota', model='Corolla', year=2020, plate="ABC-213")
        self.client.force_authenticate(user=user)
        response = self.client.delete(reverse('vehicle-detail', kwargs={'pk': vehicle.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vehicle.objects.filter(pk=vehicle.pk).exists())

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access the endpoint."""
        response = self.client.get(reverse('vehicle-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
