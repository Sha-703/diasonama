from django.contrib import admin
from .models import Activity, EncadreurAssignment


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'start_date', 'end_date', 'created_by')
    list_filter = ('published',)
    search_fields = ('title', 'description')


@admin.register(EncadreurAssignment)
class EncadreurAssignmentAdmin(admin.ModelAdmin):
    list_display = ('encadreur', 'supervisor')
    search_fields = ('encadreur__username', 'supervisor__username')
