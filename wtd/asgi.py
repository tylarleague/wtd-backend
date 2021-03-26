"""
ASGI config for wtd project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
#
# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtd.settings')
#
# application = get_asgi_application()


# import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import OriginValidator
import orders.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtd.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
# })


# application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
#   "websocket": OriginValidator(
#       AuthMiddlewareStack(
#         URLRouter(
#             orders.routing.websocket_urlpatterns
#         )
#     ),
#       ["*"],
#   ),
# })

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DHANGO_SETTINGS_MODULE", "wtd.settings")
django.setup()
application = get_default_application()