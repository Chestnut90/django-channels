from django.urls import path
from chats import views

app_name = "chats"

urlpatterns = [
    path("echo/", views.echo_page),
    path("", views.index, name="index"),
    path("<str:room_pk>/chat/", views.room_chat, name="room_chat"),
    path("new/", views.room_new, name="room_new"),
]
