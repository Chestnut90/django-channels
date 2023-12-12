from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("signout/", views.signout, name="signout"),
]
