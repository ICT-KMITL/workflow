from channels.generic import websockets

from django.http import HttpResponse
from . import listeners, exceptions
from channels.auth import channel_session_user_from_http

from channels.handler import AsgiHandler
import json
from channels import Group


class EventListenerMixin:
    """
    Add some behavior to the consumer to mananage event listener
    """
    event_listener_manager = listeners.EventListenerManager()
    event_listener_category = None

    def __init__(self, *args, **kwargs):
        if not self.event_listener_category:
            raise exceptions.EventListenerNotCategorized

    @property
    def event_listeners(self):
        return self.event_listener_manager.get_event_listeners(
            self.event_listener_category
        )

    def run(self, method_name, *args, **kwargs):
        for event_listener in self.event_listeners:
            getattr(event_listener, method_name)(*args, **kwargs)


class MessageConsumer(websockets.JsonWebsocketConsumer, EventListenerMixin):
    """
    Manages message through a websocket.
    """
    strict_ordering = True
    event_listener_category = "messages"

    def connection_groups(self, **kwargs):
        return ["chat"]

    def receive(self, message, **kwargs):
        self.run("pre_receive")
        self.group_send(self.connection_groups()[0], message)
        self.run("post_receive")


class ChannelConsumer(websockets.JsonWebsocketConsumer, EventListenerMixin):
    """
    Manages the channels states through a websocket.
    """
    strict_ordering = False
    event_listener_category = "channels"

    def connection_groups(self, **kwargs):
        return ["chat"]

    def receive(self, message, **kwargs):
        self.run("pre_receive")
        #Group("%s" % < user >).add(message.reply_channel)
        self.group_send(self.connection_groups()[0], message)
        self.run("post_receive")
'''
@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group("User-%s" % message.user.username[0]).add(message.reply_channel)
    Group("all_users").add(message.reply_channel)
def ws_message(message):
    pass

def ws_disconnect(message):
    Group("all_users").discard(message.reply_channel)
'''