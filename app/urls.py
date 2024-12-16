# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),  # Bosh sahifa
    path('add_user/', views.add_user, name='add_user'),  # Yuz qo'shish sahifasi
    # path('video_feed/', views.video_feed, name='video_feed'),  # Video oqimi
    path('run_face_recognition/', views.run_face_recognition, name='run_face_recognition'),  # Yuzni aniqlash
    # path('user_page/', views.user_page, name='user_page'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('face/', views.face, name='face'),
    path('', views.home, name='home'),
    path('main/', views.main, name='main'),
]
