from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from .models import Message
from django.contrib import messages
from django.db.models import Q


def is_visionnaire(user):
    return user.is_superuser or user.groups.filter(name='visionnaire').exists()


@login_required
def inbox_list(request):
    user = request.user
    # messages visible if broadcast_all OR any recipient_group is in user's groups OR sender is user
    user_group_ids = list(user.groups.values_list('id', flat=True))
    qs = Message.objects.filter(Q(broadcast_all=True) | Q(sender=user) | Q(recipient_groups__in=user_group_ids)).distinct()
    return render(request, 'inbox/list.html', {'messages': qs})


@login_required
@user_passes_test(is_visionnaire)
def inbox_create(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        broadcast_all = bool(request.POST.get('broadcast_all'))
        sel_groups = request.POST.getlist('groups')

        m = Message.objects.create(sender=request.user, subject=subject or '', body=body or '', broadcast_all=broadcast_all)
        if sel_groups and not broadcast_all:
            for gid in sel_groups:
                try:
                    g = Group.objects.get(pk=int(gid))
                    m.recipient_groups.add(g)
                except Exception:
                    continue
        messages.success(request, 'Message envoyé.')
        return redirect('inbox_list')

    return render(request, 'inbox/create.html', {'groups': groups})
