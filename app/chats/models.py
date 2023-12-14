from asgiref.sync import async_to_sync

from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import post_delete
from django.conf import settings

from config.extended_json import ExtendedJSONDecoder, ExtendedJSONEncoder

from channels.layers import get_channel_layer


class OnlineUserMixin(models.Model):
    class Meta:
        abstract = True

    online_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="RoomMember",
        blank=True,
        related_name="joined_rooms",
    )

    def online_users(self) -> QuerySet:
        return self.online_user_set.all()

    def online_usernames(self) -> list[str]:
        queryset = self.online_users().values_list("username", flat=True)
        return list(queryset)

    def is_joined_user(self, user) -> bool:
        return self.online_users().filter(id=user.id).exists()

    def user_join(self, channel_name, user) -> bool:
        try:
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            room_member = RoomMember(room=self, user=user)

        is_new_join = len(room_member.channel_names) == 0
        room_member.channel_names.add(channel_name)

        if room_member.id is None:
            room_member.save()
        else:
            room_member.save(update_fields=["channel_names"])

        return is_new_join

    def user_leave(self, channel_name, user) -> bool:
        try:
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            return True

        room_member.channel_names.remove(channel_name)
        if not room_member.channel_names:
            room_member.delete()
            return True
        else:
            room_member.save(update_fields=["channel_names"])
            return False


class Room(OnlineUserMixin, models.Model):

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


class RoomMember(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
    )

    channel_names = models.JSONField(
        default=set,
        encoder=ExtendedJSONEncoder,
        decoder=ExtendedJSONDecoder,
    )
