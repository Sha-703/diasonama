from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='activities_index'),
    path('supervisor/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('supervisor/create-report/', views.supervisor_create_report, name='supervisor_create_report'),
]
