from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from orders.consumers import UpdatesConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    # url(r"^messages/(?P<username>[\w.@+-]+)/$", StatusConsumer),
                    url(r"^updates/", UpdatesConsumer),
                    # url(r"^listItem/", ListItemConsumer),
                ]
            )
        )
    )
})