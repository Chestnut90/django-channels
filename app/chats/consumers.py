from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer

from chats.models import Room


class EchoConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        self.send(f"Echo : {text_data}")


class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = ""
        self.room = None

    def connect(self):

        user = self.scope["user"]

        if user is None or not user.is_authenticated:
            self.close()

        room_pk = self.scope["url_route"]["kwargs"]["room_pk"]

        try:
            self.room = Room.objects.get(id=room_pk)
        except Room.DoesNotExist:
            self.close()
            return

        self.group_name = self.room.chats_group_name
        is_new_join = self.room.user_join(self.channel_name, user)

        if is_new_join:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "chats.user.join",
                    "username": user.username,
                },
            )

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

        user = self.scope["user"]
        if self.room is not None:
            is_last_leave = self.room.user_leave(self.channel_name, user)
            if is_last_leave:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        "type": "chats.user.leave",
                        "username": user.username,
                    },
                )

    def chats_user_join(self, messages: dict):
        self.send_json(
            {
                "type": "chats.user.join",
                "username": messages["username"],
            }
        )

    def chats_user_leave(self, messages: dict):
        self.send_json(
            {
                "type": "chats.user.leave",
                "username": messages["username"],
            }
        )

    def receive_json(self, content, **kwargs):
        if "chats.message" != content["type"]:
            raise Exception("invalid event type")

        user = self.scope["user"]
        message = content["message"]
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "chats.message",
                "message": message,
                "sender": user.username,
            },
        )

    def chats_message(self, messages):
        self.send_json(
            {
                "type": "chats.message",
                "message": messages["message"],
                "sender": messages["sender"],
            }
        )

    def chats_room_deleted(self, messages: dict):
        self.close(code=4000)
