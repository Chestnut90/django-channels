from asgiref.sync import async_to_sync
from django.utils.functional import cached_property
from channels.layers import get_channel_layer


class ChannelLayerGroupSendMixin:
    channel_layer_group_name = None

    @cached_property
    def channel_layer(self):
        return get_channel_layer()

    def channel_layer_group_send(self, message: dict):
        async_to_sync(self.channel_layer.group_send)(
            self.channel_layer_group_name,
            message,
        )
