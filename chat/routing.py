from django.urls import re_path # regular expression path
from . import consumers

# we have to call as_asgi() class method when routing consumers. returns an ASGI wrapper application that instantiates a new consumer interface for each connection or scope
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatRoomConsumer.as_asgi()),
]