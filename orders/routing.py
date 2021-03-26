from django.urls import path, re_path
from . import consumers

from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
# ]
# # ws_urlpatterns = [
# websocket_urlpatterns = [
#     re_path('updates/', consumers.UpdatesConsumer)
#     # re_path(r'updates/', consumers.UpdatesConsumer.as_asgi()),
# ]


# # from channels.routing import ProtocolTypeRouter
# from django.conf.urls import url
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
#
# from orders.consumers import UpdatesConsumer
#
# application = ProtocolTypeRouter({
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 [
#                     # url(r"^messages/(?P<username>[\w.@+-]+)/$", StatusConsumer),
#                     url(r"^updates/", UpdatesConsumer),
#                     # url(r"^listItem/", ListItemConsumer),
#                 ]
#             )
#         )
#     )
# })