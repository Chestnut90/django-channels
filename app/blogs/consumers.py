import json

from channels.generic.websocket import WebsocketConsumer


class LivePostConsumer(WebsocketConsumer):

    groups = ["livepost"]

    def _sender(self, event: dict):
        self.send(json.dumps(event))

    def livepost_post_created(self, event: dict):
        self._sender(event)

    def livepost_post_updated(self, event: dict):
        self._sender(event)

    def livepost_post_deleted(self, event: dict):
        self._sender(event)
