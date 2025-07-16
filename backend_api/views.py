from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle, Booking
from .serializers import VehicleSerializer, BookingSerializer
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(vehicle__user=self.request.user)

    def perform_create(self, serializer):
        vehicle = serializer.validated_data['vehicle']
        if vehicle.user != self.request.user:
            raise PermissionDenied("You can only book your own vehicles.")
        serializer.save()


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
