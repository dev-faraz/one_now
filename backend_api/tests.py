from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class VehicleTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.token = self.client.post('/login/', {'username': 'testuser', 'password': 'testpass'}).data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_add_vehicle(self):
        response = self.client.post('/vehicles/', {'make': 'Toyota', 'model': 'Corolla', 'year': 2020, 'plate': 'ABC123'})
        self.assertEqual(response.status_code, 201)