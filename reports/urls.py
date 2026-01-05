from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportListView.as_view(), name='reports_list'),
    path('create/', views.ReportCreateView.as_view(), name='reports_create'),
    path('my/', views.MyReportsListView.as_view(), name='reports_my'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='reports_detail'),
    path('<int:pk>/edit/', views.ReportUpdateView.as_view(), name='reports_edit'),
    path('<int:pk>/delete/', views.ReportDeleteView.as_view(), name='reports_delete'),
]
