import json

from channels.generic.websocket import WebsocketConsumer


class LivePostConsumer(WebsocketConsumer):

    groups = ["livepost"]

    def _sender(self, event: dict):
        self.send(json.dumps(event))

    def livepost_post_created(self, event: dict):
        print("1receive, ", event)
        self._sender(event)

    def livepost_post_updated(self, event: dict):
        print("1updated, ", event)
        self._sender(event)

    def livepost_post_deleted(self, event: dict):
        print("d1eleted, ", event)
        self._sender(event)
