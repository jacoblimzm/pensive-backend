"""
ASGI config for pensive project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# similar to how "urls" in the project folder imports urls from various apps that extend the paths,
# "routing" in the project folder will import routes from varoius apps which have their own "routing" files
# that will extend the BASE path of routing
import django
django.setup() # DJANGO_SETTINGS_MODULE must be defined in environement variables
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing # importing from chat folder
import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pensive.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns # looks in chat app folder for routing.py with a constant called websocket_urlpatterns
            )
    )
})

# application = get_asgi_application()
