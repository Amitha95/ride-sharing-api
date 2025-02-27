import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Ride

class RideTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        self.room_group_name = f"ride_{self.ride_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data['latitude']
        longitude = data['longitude']

        ride = await sync_to_async(Ride.objects.get)(id=self.ride_id)
        ride.current_latitude = latitude
        ride.current_longitude = longitude
        await sync_to_async(ride.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "send_update", "latitude": latitude, "longitude": longitude}
        )

    async def send_update(self, event):
        await self.send(text_data=json.dumps({
            "latitude": event["latitude"],
            "longitude": event["longitude"]
        }))
