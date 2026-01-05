from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('private/', views.private_dashboard, name='private'),
    path('private/manage-users/', views.manage_users, name='manage_users'),
    path('private/manage-users/ajax-toggle/', views.manage_users_ajax_toggle, name='manage_users_ajax_toggle'),
]
