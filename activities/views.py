from django.shortcuts import render

from .models import Activity
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import EncadreurAssignment
import secrets
from reports.models import Report, Photo
from .models import Activity as ActivityModel


def is_superviseur(user):
    return user.is_superuser or user.groups.filter(name='superviseur').exists()


@login_required
@user_passes_test(is_superviseur)
def supervisor_dashboard(request):
    """Supervisor interface to create encadreurs and assign/unassign them.

    Actions (POST):
    - action=create_encadreur: fields `username`, `email`, `first_name`, `last_name`
    - action=assign: field `user_id` (assign existing user as encadreur to current supervisor)
    - action=unassign: field `assignment_id` (remove assignment)
    """
    User = get_user_model()

    # ensure groups exist
    encadreur_group, _ = Group.objects.get_or_create(name='encadreur')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create_encadreur':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            if not username:
                messages.error(request, 'Le nom d\'utilisateur est requis.')
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Nom d\'utilisateur déjà pris.')
                else:
                    # generate a temporary password
                    temp_pwd = secrets.token_urlsafe(8)
                    new_user = User.objects.create_user(username=username, email=email, password=temp_pwd,
                                                        first_name=first_name, last_name=last_name)
                    new_user.groups.add(encadreur_group)
                    # create assignment
                    EncadreurAssignment.objects.create(supervisor=request.user, encadreur=new_user)
                    messages.success(request, f"Encadreur '{username}' créé. Mot de passe temporaire: {temp_pwd} (console email envoyé si activé)")
        elif action == 'assign':
            try:
                uid = int(request.POST.get('user_id'))
                u = get_object_or_404(User, pk=uid)
                u.groups.add(encadreur_group)
                EncadreurAssignment.objects.get_or_create(supervisor=request.user, encadreur=u)
                messages.success(request, f"{u.username} assigné comme encadreur.")
            except Exception as e:
                messages.error(request, 'Impossible d\'assigner l\'utilisateur.')
        elif action == 'unassign':
            try:
                aid = int(request.POST.get('assignment_id'))
                a = get_object_or_404(EncadreurAssignment, pk=aid, supervisor=request.user)
                a.delete()
                messages.success(request, 'Encadreur désassigné.')
            except Exception:
                messages.error(request, 'Impossible de désassigner.')
        return redirect('supervisor_dashboard')

    # GET: list current assignments and possible users to assign
    assignments = EncadreurAssignment.objects.filter(supervisor=request.user).select_related('encadreur')
    # users that are encadreurs but not assigned to this supervisor
    encadreur_qs = User.objects.filter(groups__name='encadreur').exclude(pk__in=[a.encadreur.pk for a in assignments])
    # also allow assigning any existing user
    available_users = User.objects.exclude(pk=request.user.pk).order_by('username')[:200]
    activities = ActivityModel.objects.order_by('-start_date')[:50]

    return render(request, 'activities/supervisor.html', {
        'assignments': assignments,
        'encadreurs': encadreur_qs,
        'available_users': available_users,
        'activities': activities,
    })


@login_required
@user_passes_test(is_superviseur)
def supervisor_create_report(request):
    """Quick report creation endpoint for supervisors (from dashboard)."""
    if request.method != 'POST':
        return redirect('supervisor_dashboard')
    # fields: date, activity_id, text, status
    date = request.POST.get('date')
    activity_id = request.POST.get('activity')
    text = request.POST.get('text')
    status = request.POST.get('status') or 'draft'
    activity = None
    if activity_id:
        try:
            activity = ActivityModel.objects.get(pk=int(activity_id))
        except Exception:
            activity = None

    report = Report.objects.create(author=request.user, date=date or None, activity=activity, text=text or '', status=status, supervisor=request.user)
    # optional photo
    photo = request.FILES.get('photo')
    if photo:
        Photo.objects.create(report=report, image=photo)
    messages.success(request, 'Rapport créé.')
    return redirect('supervisor_dashboard')


def index(request):
    """Render a simple activities listing page.

    Shows recent activities ordered by start_date (newest first). If there
    are no activities, a friendly message is displayed.
    """
    activities = Activity.objects.order_by('-start_date')[:50]
    return render(request, 'activities/list.html', {'activities': activities})
