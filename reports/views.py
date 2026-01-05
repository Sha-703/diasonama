from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Report
from .models import Photo
from .forms import ReportForm
from django.contrib.auth.mixins import AccessMixin
from django.core.paginator import Paginator
from django.db import models
from activities.models import EncadreurAssignment


class ReportListView(ListView):
    model = Report
    template_name = 'reports/list.html'
    context_object_name = 'reports'
    paginate_by = 20


class MyReportsListView(LoginRequiredMixin, ListView):
    """List reports for the current user.

    - Encadreur: shows reports authored by the user.
    - Superviseur: shows reports authored by the superviseur and by encadreurs assigned to them.
    - Other users: shows reports authored by the user.
    """
    model = Report
    template_name = 'reports/my_reports.html'
    context_object_name = 'reports'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        qs = Report.objects.none()
        if user.groups.filter(name='superviseur').exists() or user.is_superuser:
            # reports authored by this supervisor OR by encadreurs assigned to them
            enc_ids = EncadreurAssignment.objects.filter(supervisor=user).values_list('encadreur_id', flat=True)
            qs = Report.objects.filter(models.Q(author=user) | models.Q(author__id__in=list(enc_ids))).order_by('-date')
        else:
            qs = Report.objects.filter(author=user).order_by('-date')
        return qs


class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'


class ReportCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/form.html'
    success_url = reverse_lazy('reports_my')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # handle optional uploaded photo
        photo = self.request.FILES.get('photo')
        if photo:
            Photo.objects.create(report=self.object, image=photo)
        return response

    def test_func(self):
        user = self.request.user
        # allow encadreur, superviseur, administrateur
        return user.groups.filter(name__in=['encadreur', 'superviseur', 'administrateur']).exists() or user.is_superuser


class ReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/form.html'
    success_url = reverse_lazy('reports_my')

    def test_func(self):
        user = self.request.user
        report = self.get_object()
        return user == report.author or user.is_superuser or user.groups.filter(name='superviseur').exists()
    
    def form_valid(self, form):
        response = super().form_valid(form)
        photo = self.request.FILES.get('photo')
        if photo:
            Photo.objects.create(report=self.object, image=photo)
        return response


class ReportDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Report
    template_name = 'reports/confirm_delete.html'
    success_url = reverse_lazy('reports_list')

    def test_func(self):
        user = self.request.user
        report = self.get_object()
        return user == report.author or user.is_superuser or user.groups.filter(name='superviseur').exists()

