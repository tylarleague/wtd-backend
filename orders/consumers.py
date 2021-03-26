import json
from random import randint
from time import sleep



from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer


# class UpdatesConsumer(AsyncJsonWebsocketConsumer):
    # async def connect(self):
    #     self.accept()
    #
    #     for i in range(1000):
    #         self.send(json.dumps({'message': randint(1, 100)}))
    #         sleep(1)

class UpdatesConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("update_order", self.channel_name)
        print(f"Added {self.channel_name} channel to update_order")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("announcement", self.channel_name)
        print(f"Removed {self.channel_name} channel to announcement")

    async def change_update_order(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")
