from django.urls import path
from blogs import views

urlpatterns = [
    path("posts/", views.posts_index),
    path("posts/<int:id>/", views.posts_partial, name="post_retrieve"),
]
