from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ride

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {'email': {'required': True}}

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['pickup_location', 'dropoff_location', 'pickup_latitude', 'pickup_longitude', 'status', 'rider']
        extra_kwargs = {'rider': {'read_only': True}}  # Ensure 'rider' is read-only

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['rider'] = request.user
        return super().create(validated_data)
