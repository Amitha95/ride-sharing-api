from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rideapp.models import Ride

class RideTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
    
    def test_create_ride(self):
        response = self.client.post("/api/rides/", {
            "pickup_location": "Location A",
            "dropoff_location": "Location B"
        })
        self.assertEqual(response.status_code, 201)

    def test_update_ride_status(self):
        ride = Ride.objects.create(rider=self.user, pickup_location="A", dropoff_location="B")
        response = self.client.patch(f"/api/rides/{ride.id}/update_status/", {"status": "completed"})
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        User.objects.create_user(username="testuser", password="password")
        response = self.client.post("/users/login/", {"username": "testuser", "password": "password"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
