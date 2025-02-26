from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RideTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        ride_id = data.get("ride_id")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Broadcast location update
        await self.channel_layer.group_send(
            f"ride_{ride_id}",
            {
                "type": "ride_location",
                "latitude": latitude,
                "longitude": longitude
            }
        )

    async def ride_location(self, event):
        await self.send(text_data=json.dumps(event))
