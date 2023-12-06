from django.db import models
from django.db.models.signals import post_save, post_delete
from django.urls import reverse

from blogs.mixins import ChannelLayerGroupSendMixin


class Post(ChannelLayerGroupSendMixin, models.Model):

    channel_layer_group_name = "livepost"

    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        ordering = ["-id"]


def post__on_post_save(instance: Post, created: bool, **kwargs):
    status = "created" if created else "updated"
    message_type = f"livepost.post.{status}"
    post_partial_url = reverse("post_partial", args=[instance.pk])

    instance.channel_layer_group_send(
        {
            "type": message_type,
            "id": instance.pk,
            "post_partial_url": post_partial_url,
        }
    )


post_save.connect(
    post__on_post_save,
    sender=Post,
    dispatch_uid="post__on_post_save",
)


def post__on_post_delete(instance: Post, **kwargs):
    instance.channel_layer_group_send(
        {
            "type": "livepost.post.deleted",
            "id": instance.pk,
        }
    )


post_delete.connect(
    post__on_post_delete,
    sender=Post,
    dispatch_uid="post__on_post_delete",
)
