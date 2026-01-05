from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group


class Profile(models.Model):
    ROLE_VISIONNAIRE = 'visionnaire'
    ROLE_ENCADREUR = 'encadreur'
    ROLE_INVESTISSEUR = 'investisseur'
    ROLE_SUPERVISEUR = 'superviseur'
    ROLE_ADMIN = 'administrateur'

    ROLE_CHOICES = [
        (ROLE_VISIONNAIRE, 'Visionnaire'),
        (ROLE_ENCADREUR, 'Encadreur'),
        (ROLE_INVESTISSEUR, 'Investisseur'),
        (ROLE_SUPERVISEUR, 'Superviseur'),
        (ROLE_ADMIN, 'Administrateur'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'

    def __str__(self):
        return f"{self.user.get_username()} ({self.role or '—'})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # create an empty profile for new users
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def sync_profile_group(sender, instance, **kwargs):
    """Keep Django `Group` membership in sync with Profile.role.

    When a Profile has `role` set, ensure the user is member of the
    corresponding Group, and remove other role-groups.
    """
    role_names = [c[0] for c in Profile.ROLE_CHOICES]
    # create/get the target group
    if instance.role:
        target_group, _ = Group.objects.get_or_create(name=instance.role)
    else:
        target_group = None

    for rn in role_names:
        g, _ = Group.objects.get_or_create(name=rn)
        if target_group and g.name == target_group.name:
            if not instance.user.groups.filter(pk=g.pk).exists():
                instance.user.groups.add(g)
        else:
            if instance.user.groups.filter(pk=g.pk).exists():
                instance.user.groups.remove(g)
