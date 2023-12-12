from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# Create your views here.

signin = LoginView.as_view(
    template_name="partials/form.html",
    next_page="users:profile",
    extra_context={
        "form_name": "Sign-In",
        "submit_label": "Sign-In",
    },
)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"


signup = CreateView.as_view(
    form_class=UserCreationForm,
    template_name="partials/form.html",
    extra_context={
        "form_name": "Sign-Up",
        "submit_label": "Sign-Up",
    },
    success_url=reverse_lazy("users:signin"),
)

signout = LogoutView.as_view(
    next_page="users:signin",
)
