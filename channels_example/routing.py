from channels.routing import route
from . import consumers

channel_routing = [
    #route("http.request", "channels_example.consumers.http_consumer"), --It will proxy any http request
    route("websocket.connect", consumers.ws_connect),
    route("websocket.receive", consumers.ws_message),
    route("websocket.disconnect", consumers.ws_disconnect),
]