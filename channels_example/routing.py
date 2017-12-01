from channels.routing import route
from channels_example.consumers import ws_message

channel_routing = [
    route("websocket.receive", ws_message),
    route("http.request", "channels_example.consumers.http_consumer"),
]