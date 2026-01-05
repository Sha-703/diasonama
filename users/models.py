from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model minimal implementation.

    Extends AbstractUser so Django knows about `users.User` when
    `AUTH_USER_MODEL = 'users.User'` is set in settings.
    """
    # Add custom fields here if needed later
    pass
