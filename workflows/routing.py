'''
from channels.routing import route
from workflows.consumers import ws_connect,ws_message,ws_disconnect
'''
from . import consumers, consumer1, consumer2, consumer3


channel_routing = [


    #consumers.ChannelConsumer.as_route(path=r'^/chat/'),
    consumers.ChannelConsumer.as_route(path=r'^/chat/'),
    consumer1.ChannelConsumer.as_route(path=r'^/chat1/'),
    consumer2.ChannelConsumer.as_route(path=r'^/chat2/'),
    consumer3.ChannelConsumer.as_route(path=r'^/chat3/'),

]

