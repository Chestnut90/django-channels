from django.urls import path

from blogs.consumers import LivePostConsumer

websocket_urlpatterns = [
    path("ws/livepost/", LivePostConsumer.as_asgi()),
]
