from django.urls import path
from . import views

urlpatterns = [
    path('', views.openCamera, name='open-camera'),
    path('output/', views.detect, name='output'),
    path('player/', views.detect, name='mood-detect-play'),
]