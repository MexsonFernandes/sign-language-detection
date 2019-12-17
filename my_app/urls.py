from django.urls import path
from . import views

urlpatterns = [
    path('', views.openCamera, name='open-camera'),
<<<<<<< HEAD
    path('output/', views.detect, name='output'),
=======
    path('player/', views.detect, name='mood-detect-play'),
>>>>>>> 598affdaf1f42f8d211c1ae923a1f089066c7633
]