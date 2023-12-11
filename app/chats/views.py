from django.shortcuts import render


def echo_page(request):
    return render(request, "chats/echo_page.html")


def index(request):
    return render(request, "chats/index.html")


def room_chat(request, room_name):
    return render(
        request,
        "chats/room_chat.html",
        {
            "room_name": room_name,
        },
    )
