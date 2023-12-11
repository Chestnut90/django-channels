from django import forms
from chats.models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name"]
