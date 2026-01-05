from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('activities/', include('activities.urls')),
    path('reports/', include('reports.urls')),
    path('inbox/', include('inbox.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers (useful when DEBUG = False)
handler404 = 'diasonama.views.custom_404'
handler403 = 'diasonama.views.custom_403'
handler500 = 'diasonama.views.custom_500'
