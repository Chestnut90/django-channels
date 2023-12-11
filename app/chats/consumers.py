from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer


class EchoConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        self.send(f"Echo : {text_data}")


class ChatConsumer(JsonWebsocketConsumer):

    GROUP_NAME = "square"
    groups = [GROUP_NAME]

    def receive_json(self, content, **kwargs):
        if "chats.message" != content["type"]:
            raise Exception("invalid event type")

        message = content["message"]
        async_to_sync(self.channel_layer.group_send)(
            self.GROUP_NAME,
            {
                "type": "chats.message",
                "message": message,
            },
        )

    def chats_message(self, messages):
        self.send_json(
            {
                "type": "chats.message",
                "message": messages["message"],
            }
        )
