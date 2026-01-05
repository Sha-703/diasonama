from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox_list, name='inbox_list'),
    path('create/', views.inbox_create, name='inbox_create'),
]
