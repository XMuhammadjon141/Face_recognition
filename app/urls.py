from django.urls import path
from . import views

urlpatterns = [
    path('video_feed/', views.video_feed, name='video_feed'),
    path('face/', views.face, name='face'),
    path('add_user/', views.add_user, name='add_user'),
]
