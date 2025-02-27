from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rideapp.models import Ride

class RideTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.rider = User.objects.create_user(username="rider", password="password")
        self.driver = User.objects.create_user(username="driver", password="password")
        self.client.force_authenticate(user=self.rider)
    
    def test_create_ride(self):
        response = self.client.post("/api/rides/", {
            "pickup_location": "Location A",
            "dropoff_location": "Location B"
        })
        self.assertEqual(response.status_code, 201)
    
    def test_driver_accepts_ride(self):
        """
        Driver accepts the ride.
        """
        ride = Ride.objects.create(rider=self.rider, pickup_location="A", dropoff_location="B")

        self.client.force_authenticate(user=self.driver)
        response = self.client.post(f"/api/rides/{ride.id}/accept_ride/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["ride"]["status"], "accepted")

    def test_driver_updates_location(self):
        """
        Driver updates real-time location.
        """
        ride = Ride.objects.create(rider=self.rider, pickup_location="A", dropoff_location="B", driver=self.driver, status="accepted")

        self.client.force_authenticate(user=self.driver)
        response = self.client.patch(f"/api/rides/{ride.id}/update_location/", {
            "latitude": 37.7749, "longitude": -122.4194
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(float(response.data["ride"]["current_latitude"]), 37.7749)

    def test_update_ride_status(self):
        ride = Ride.objects.create(rider=self.rider, pickup_location="A", dropoff_location="B")
        self.client.force_authenticate(user=self.driver)  # Authenticate before making request
        response = self.client.patch(f"/api/rides/{ride.id}/update_status/", {"status": "completed"})
        self.assertEqual(response.status_code, 200)
        
    def test_login_user(self):
        User.objects.create_user(username="testuser", password="password")
        response = self.client.post("/api/token/", {"username": "testuser", "password": "password"})  # Ensure correct URL
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)  # JWT should return an access token

