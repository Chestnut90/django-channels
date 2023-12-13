from asgiref.sync import async_to_sync

from django.db import models
from django.db.models.signals import post_delete
from django.conf import settings

from channels.layers import get_channel_layer


class Room(models.Model):

    name = models.CharField(max_length=100)  # duplicated

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rooms",
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def chats_group_name(self):
        return f"chats-{self.id}"


def room__post_delete(instance: Room, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        instance.chats_group_name,
        {
            "type": "chats.room.deleted",
        },
    )


# connect post delete signal
post_delete.connect(
    room__post_delete,
    sender=Room,
    dispatch_uid="room__post_delete",
)
