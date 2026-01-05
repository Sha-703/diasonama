from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'created_at', 'broadcast_all')
    list_filter = ('broadcast_all', 'recipient_groups')
    search_fields = ('subject', 'body', 'sender__username')
    filter_horizontal = ('recipient_groups',)
