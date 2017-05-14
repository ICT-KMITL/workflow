from channels.generic import websockets

from . import listeners, exceptions


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
        self.group_send(self.connection_groups()[0], message)
        self.run("post_receive")
