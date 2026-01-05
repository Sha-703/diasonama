from django.shortcuts import render


def custom_404(request, exception=None):
    """Custom 404 handler that renders `templates/404.html`."""
    return render(request, '404.html', status=404)


def custom_403(request, exception=None):
    """Custom 403 handler that renders `templates/403.html`."""
    return render(request, '403.html', status=403)


def custom_500(request):
    """Custom 500 handler that renders `templates/500.html`."""
    return render(request, '500.html', status=500)

