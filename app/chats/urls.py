from django.urls import path
from chats import views

app_name = "chats"

urlpatterns = [
    path("echo/", views.echo_page),
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room_chat, name="room_chat"),
]
