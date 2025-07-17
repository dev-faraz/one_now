from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_success(self):
        """Test successful user registration."""
        data = {'username': 'newuser', 'password': 'newpass'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully.')
        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('newpass'))

    def test_register_missing_fields(self):
        """Test registration with missing username or password."""
        # Missing password
        data = {'username': 'newuser'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username and password are required.')

        # Missing username
        data = {'password': 'newpass'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username and password are required.')

    def test_register_existing_username(self):
        """Test registration with an existing username."""
        User.objects.create_user(username='existinguser', password='existingpass')
        data = {'username': 'existinguser', 'password': 'newpass'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username already exists.')
