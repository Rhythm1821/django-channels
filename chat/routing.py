from django.urls import re_path,path

from . import consumers

websockets_urlpatterns = [
    path(r"ws/chat/<str:room_name>/",consumers.ChatConsumer.as_asgi()),
    # re_path(r"ws/chat/(?P<room_name>\w+)/$",consumers.ChatConsumer.as_asgi()),
]