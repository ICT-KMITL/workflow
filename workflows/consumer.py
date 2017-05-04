from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
import json

def ws_add(message):
    message.reply_channel.send({
        'text': json.dumps({'type': 'handshake'})
    })
    Group("users").add(message.reply_channel)

def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    #message.reply_channel.send({
    #    "text": message.content['text'],
    #})

    obj = json.loads(message.content['text'])

    if obj['type'] == "Login":
        username = obj['username']
        password = obj['password']

        if True:
            Group("users").send({
                "text": JSON.dumps({'type': 'User_Online', 'username': username}),
            })


    #Group("users").send({
    #     "text": message.content['text'],
    #})

def ws_disconnect(message):
    Group("users").discard(message.reply_channel)
    #user offline