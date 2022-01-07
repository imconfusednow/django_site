from django.urls import path
from . import views

urlpatterns = [
           path('coup', views.coup, name='coup-coup'),
        ]
