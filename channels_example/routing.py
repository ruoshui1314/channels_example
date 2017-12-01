from channels.routing import route
from channels_example.consumers import ws_message, ws_add, ws_disconnect

channel_routing = [
    route("http.request", "channels_example.consumers.http_consumer"),
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]