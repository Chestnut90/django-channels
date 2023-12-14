from django.urls import path
from chats import views

app_name = "chats"

urlpatterns = [
    path("echo/", views.echo_page),
    path("", views.index, name="index"),
    path("<int:room_pk>/chat/", views.room_chat, name="room_chat"),
    path("new/", views.room_new, name="room_new"),
    path("<int:room_pk>/delete/", views.room_delete, name="room_delete"),
    path("<int:room_pk>/members/", views.room_members, name="room_members"),
]
