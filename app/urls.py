# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Bosh sahifa
    path('add_user/', views.add_user, name='add_user'),  # Yuz qo'shish sahifasi
    path('video_feed/', views.video_feed, name='video_feed'),  # Video oqimi
    path('run_face_recognition/', views.run_face_recognition, name='run_face_recognition'),  # Yuzni aniqlash
]
