from django.db import migrations


class Migration(migrations.Migration):
    """Empty initial migration to satisfy external dependencies.

    Some other app migrations may declare a swappable dependency on
    `settings.AUTH_USER_MODEL`. When `AUTH_USER_MODEL = 'users.User'`
    but the `users` app has no migrations yet, Django raises the
    "Dependency on app with no migrations" ValueError. Providing a
    minimal initial migration resolves that during development.
    """

    initial = True

    dependencies = []

    operations = []
