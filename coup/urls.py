from django.urls import path
from . import views

urlpatterns = [
           path('', views.login, name='coup-coup_login'),
           path('game/', views.game, name='coup-coup_game'),
           path('create/<room_name>/', views.game_create, name='coup-coup_game_create')
        ]
