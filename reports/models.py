from django.db import models
from django.conf import settings


class Report(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('submitted', 'Soumis'),
        ('validated', 'Validé'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_reports')
    date = models.DateField()
    activity = models.ForeignKey('activities.Activity', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f"Rapport {self.author} - {self.date}"


class Photo(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='reports/%Y/%m/%d')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or self.image.name
