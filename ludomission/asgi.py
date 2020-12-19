"""
ASGI config for ludomission project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
#from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from game import consumers
from django.urls import re_path
from django.core.asgi import get_asgi_application
from channels.routing import get_default_application
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ludomission.settings')

django.setup()
django_asgi_app = get_asgi_application()


ws_pattern= [
    path('ws/tableData/<username>',consumers.TableData),
    path('ws/allgames/' , consumers.AllGames),
    path('ws/room/' , consumers.Room),
    path('ws/game/room/<room_name>' , consumers.ChatConsumer),
    path('ws/join/' , consumers.JoinRequest)
]

application= ProtocolTypeRouter(
   
    {
         #"http": django_asgi_app,
        'websocket':AuthMiddlewareStack(URLRouter(ws_pattern))
    }
)
