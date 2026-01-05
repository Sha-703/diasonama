from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # recipients: either broadcast_all or specific groups
    broadcast_all = models.BooleanField(default=False)
    recipient_groups = models.ManyToManyField(Group, blank=True, related_name='messages')

    def __str__(self):
        to = 'Tous' if self.broadcast_all else ','.join([g.name for g in self.recipient_groups.all()])
        return f"Message from {self.sender} to {to} - {self.subject[:40]}"

    class Meta:
        ordering = ['-created_at']
