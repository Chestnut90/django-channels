from django.urls import path
from chats.consumers import EchoConsumer, ChatConsumer

websocket_urlpatterns = [
    path("ws/echo/", EchoConsumer.as_asgi()),
    path("ws/chats/<str:room_pk>/chat/", ChatConsumer.as_asgi()),
]
