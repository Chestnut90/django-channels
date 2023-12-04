from django.urls import path
from chats import views

urlpatterns = [
    path("echo/", views.echo_page),
]
