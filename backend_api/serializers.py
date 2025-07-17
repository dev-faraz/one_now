from rest_framework import serializers
from .models import Vehicle, Booking

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'year', 'plate']
        read_only_fields = ['id']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'vehicle', 'start_date', 'end_date']
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['vehicle'] = VehicleSerializer(instance.vehicle).data
        return representation

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data