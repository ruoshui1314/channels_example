from django.http import HttpResponse
from channels.handler import AsgiHandler
import json
from channels import Group
from channels.sessions import channel_session
from urlparse import parse_qs
from .log import log

def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)

# Connected to websocket.connect
@channel_session
def ws_connect(message):
    log.debug("ws_connect")
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Parse the query string
    params = parse_qs(message.content["query_string"])
    log.debug(params)
    if b"username" in params:
        # Set the username in the session
        message.channel_session["username"] = params[b"username"][0].decode("utf8")
        # Add the user to the room_name group
        Group("chat").add(message.reply_channel)
    else:
        # Close the connection.
        message.reply_channel.send({"close": True})

# Connected to websocket.receive
@channel_session
def ws_message(message):
    log.debug("ws_message")
    log.debug(message)
    Group("chat").send({
        "text": json.dumps({
            "text": message["text"],
            "username": message.channel_session["username"],
        }),
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    log.debug("ws_disconnect")
    Group("chat").discard(message.reply_channel)