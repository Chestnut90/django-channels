from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse

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
            "room": room,
        },
    )


@login_required(login_url="users:signin")
def room_new(request):

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room: Room = form.save(commit=False)
            created_room.owner = request.user
            created_room.save()
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


@login_required(login_url="users:signin")
def room_delete(request: HttpRequest, room_pk: int) -> HttpResponse:
    room = get_object_or_404(Room, id=room_pk)

    if room.owner != request.user:
        messages.error(request, "No owner of room.")
        return redirect("chats:index")

    # only post using url
    if request.method == "POST":
        room.delete()
        messages.success(request, "Room was deleted in success.")
        return redirect("chats:index")

    # get
    return render(
        request,
        template_name="chats/room_delete_confirm.html",
        context={
            "room": room,
        },
    )


@login_required(login_url="users:signin")
def room_members(request: HttpRequest, room_pk: int) -> HttpResponse:
    room = get_object_or_404(Room, id=room_pk)

    if not room.is_joined_user(request.user):
        return HttpResponse("Unauthorized user", status=401)

    usernames = room.online_usernames()
    return JsonResponse(
        {
            "usernames": usernames,
        }
    )
