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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ludomission.settings')



ws_pattern= [
    path('ws/tableData/',consumers.TableData),
    path('ws/room/' , consumers.Room),
    path('ws/game/room/<room_name>' , consumers.ChatConsumer)
]

application= ProtocolTypeRouter(
    {
        'websocket':AuthMiddlewareStack(URLRouter(ws_pattern))
    }
)
