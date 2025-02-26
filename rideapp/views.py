from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Ride
from .serializers import UserSerializer, RideSerializer
from math import radians, cos, sin, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km


class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "User registered successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)  # Logs the user in for session-based authentication
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all().order_by('-created_at')
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(f"Creating ride for user: {self.request.user}")  # Debug log
        serializer.save(rider=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        ride = self.get_object()
        if ride.rider != request.user and ride.driver != request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get("status")
        if new_status in dict(Ride.STATUS_CHOICES):
            ride.status = new_status
            ride.save()
            return Response({"message": "Status updated successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def match_ride(self, request):
        user_lat = request.data.get("pickup_latitude")
        user_lon = request.data.get("pickup_longitude")

        if user_lat is None or user_lon is None:
            return Response({"error": "Latitude and Longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

        user_lat = float(user_lat)
        user_lon = float(user_lon)

        available_rides = Ride.objects.filter(status="pending")

        if not available_rides.exists():
            return Response({"error": "No rides available"}, status=status.HTTP_404_NOT_FOUND)

        available_rides = [
            ride for ride in available_rides 
            if ride.pickup_latitude is not None and ride.pickup_longitude is not None
        ]

        if not available_rides:
            return Response({"error": "No valid rides with pickup coordinates"}, status=status.HTTP_404_NOT_FOUND)

        # Find the nearest ride using Haversine distance
        nearest_ride = min(
            available_rides,
            key=lambda ride: haversine(user_lat, user_lon, ride.pickup_latitude, ride.pickup_longitude)
        )

        nearest_ride.driver = request.user
        nearest_ride.status = "accepted"
        nearest_ride.save()

        return Response(RideSerializer(nearest_ride).data, status=status.HTTP_200_OK)

