from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


@login_required
def private_dashboard(request):
    """Simple private dashboard showing role-specific links.

    This view ensures the standard groups exist and then decides which
    sections to show based on group membership.
    """
    # Ensure groups exist (idempotent)
    group_names = ['visionnaire', 'encadreur', 'investisseur', 'superviseur', 'administrateur']
    for name in group_names:
        Group.objects.get_or_create(name=name)

    user = request.user
    roles = {name: user.groups.filter(name=name).exists() for name in group_names}

    return render(request, 'private/dashboard.html', {'roles': roles})


from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model


@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
    """Small admin interface to assign/remove role groups for users.

    Accessible only to superusers. Displays users and checkboxes for
    known role groups. Submitting updates group membership.
    """
    User = get_user_model()
    group_names = ['visionnaire', 'encadreur', 'investisseur', 'superviseur', 'administrateur']
    groups = [Group.objects.get_or_create(name=n)[0] for n in group_names]

    if request.method == 'POST':
        # incoming form contains user_<id> fields with comma-separated group names
        for u in User.objects.all():
            key = f'user_{u.pk}'
            vals = request.POST.getlist(key)
            # remove all role groups then add selected
            for g in groups:
                if g in u.groups.all() and g.name not in vals:
                    u.groups.remove(g)
                if g.name in vals and g not in u.groups.all():
                    u.groups.add(g)
        from django.contrib import messages
        messages.success(request, 'Membres mis à jour.')

    users = User.objects.all().order_by('username')
    return render(request, 'pages/manage_users.html', {'users': users, 'groups': groups})


from django.http import JsonResponse, HttpResponseForbidden


@user_passes_test(lambda u: u.is_superuser)
def manage_users_ajax_toggle(request):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseForbidden()
    username = request.POST.get('username')
    role = request.POST.get('role')
    action = request.POST.get('action')  # 'add' or 'remove'
    if not username or not role or action not in ('add', 'remove'):
        return JsonResponse({'ok': False, 'error': 'invalid parameters'}, status=400)
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'user not found'}, status=404)

    group, _ = Group.objects.get_or_create(name=role)
    if action == 'add':
        user.groups.add(group)
    else:
        user.groups.remove(group)
    return JsonResponse({'ok': True})
