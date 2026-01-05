from django.db import models
from django.conf import settings


class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    published = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='activities')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class EncadreurAssignment(models.Model):
    """Assign an encadreur (user) to a supervisor (user).

    A supervisor can assign multiple encadreurs to themselves. This model
    is minimal and used for the supervisor UI.
    """
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='supervised_encadreurs')
    encadreur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_supervisors')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('supervisor', 'encadreur'),)

    def __str__(self):
        return f"{self.encadreur} assigned to {self.supervisor}"
