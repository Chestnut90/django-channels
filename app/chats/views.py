from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from chats.models import Room
from chats.forms import RoomForm


def echo_page(request):
    return render(request, "chats/echo_page.html")


def index(request):
    queryset = Room.objects.all()
    return render(
        request,
        "chats/index.html",
        context={
            "rooms": queryset,
        },
    )


@login_required(login_url="users:signin")
def room_chat(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    return render(
        request,
        "chats/room_chat.html",
        {
            "room_name": room.name,
        },
    )


@login_required(login_url="users:signin")
def room_new(request):

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room = form.save()
            return redirect("chats:room_chat", created_room.pk)

    else:
        form = RoomForm()

    return render(
        request,
        "chats/room_form.html",
        {
            "form": form,
        },
    )
