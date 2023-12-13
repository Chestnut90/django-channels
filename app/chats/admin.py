from django.contrib import admin

from chats.models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
