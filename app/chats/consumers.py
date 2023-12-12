from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer


class EchoConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        self.send(f"Echo : {text_data}")


class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = ""

    def connect(self):

        user = self.scope["user"]

        if user is None or not user.is_authenticated:
            self.close()

        room_name = self.scope["url_route"]["kwargs"]["room_pk"]
        self.group_name = f"chats-{room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, code):

        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name,
            )

    def receive_json(self, content, **kwargs):
        if "chats.message" != content["type"]:
            raise Exception("invalid event type")

        message = content["message"]
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
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
