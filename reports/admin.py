from django.contrib import admin
from .models import Report, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('author', 'date', 'status', 'activity')
    list_filter = ('status', 'date')
    search_fields = ('author__username', 'text')
    inlines = [PhotoInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('report', 'image', 'uploaded_at')
