from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

plate_validator = RegexValidator(
    regex=r'^[A-Z]{1,4}-\d{1,4}$',
    message='Plate must be in the format ABC-123 (3 uppercase letters, a dash, and 3 digits).'
)
class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    plate = models.CharField(max_length=20, unique=True, validators=[plate_validator])


    def clean(self):
        current_year = date.today().year
        if self.year > current_year:
            raise ValidationError("Year cannot be in the future.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate})"

def start_date_validator(value):
    if timezone.is_naive(value):
        value = timezone.make_aware(value)
    if value < timezone.now():
        raise ValidationError('Start date must be on or after the current time.')

class Booking(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateTimeField(validators=[start_date_validator])
    end_date = models.DateTimeField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.vehicle} from {self.start_date} to {self.end_date}"