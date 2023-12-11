from django.urls import path
from chats.consumers import EchoConsumer, ChatConsumer

websocket_urlpatterns = [
    path("ws/echo/", EchoConsumer.as_asgi()),
    path("ws/chats/<str:room_name>/", ChatConsumer.as_asgi()),
]
