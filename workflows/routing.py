from . import consumers


channel_routing = [
    consumers.ChannelConsumer.as_route(path=r'^/chat/'),
]
