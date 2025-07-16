from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    plate = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate})"


class Booking(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Booking for {self.vehicle} from {self.start_date} to {self.end_date}"