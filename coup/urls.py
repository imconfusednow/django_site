from django.urls import path
from . import views

urlpatterns = [
           path('', views.coup_login, name='coup-coup_login'),
           path('game', views.game, name='coup-coup_game'),
        ]
