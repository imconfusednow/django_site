from django.urls import path
from . import views

urlpatterns = [  
           path('', views.cv, name='mywork-cv'),
           path('cv', views.cv, name='mywork-cv'),
           path('ecommerce_example', views.ecommerce, name='mywork-ecommerce'),
           path('projects', views.projects, name='mywork-projects'),
           path('contact', views.contact, name='mywork-contact'),
           path('search', views.search, name='mywork-search'),
        ]
