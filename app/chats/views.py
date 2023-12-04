from django.shortcuts import render


def echo_page(request):
    return render(request, "chats/echo_page.html")
