from django.contrib import admin
from django.urls import path
from .views import (noticia, video, sobre, home, play_video, view_noticia)

urlpatterns = [
    path('', home, name="home"),
    path('noticias/', noticia, name="noticias"),
    path('noticia/<int:id>/', view_noticia, name='view_noticia'),
    path('videos/', video, name="videos"),
    path('video/<int:id>/', play_video, name="play_video"),
    path('sobre/', sobre, name="sobre")
]