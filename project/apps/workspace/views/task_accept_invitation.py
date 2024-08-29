from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.db import IntegrityError
from django.shortcuts import render

from ..models import (
    TaskAssignedMember,
    Task,
    TaskInvitation
)


User = get_user_model()


def task_accept_invitation(request, uid, email, token):
    try:
        task_id = urlsafe_base64_decode(uid).decode()
        decoded_email = urlsafe_base64_decode(email).decode()
        task = get_object_or_404(Task, id=task_id)
        invitation = get_object_or_404(TaskInvitation, task=task, token=token)

        # Add the user to the workspace members (assuming user is authenticated)
        user = User.objects.get(email=decoded_email) # or use the email to find the user
        task_member = TaskAssignedMember.objects.create(task=task, role='Adi üzv', user=user)
        task_member.save()

        # Delete the invitation or mark it as accepted
        invitation.is_accepted = True
        invitation.save()

        # return redirect('workspace-detail', pk=workspace.id)  # Redirect to the workspace page
        return render(request, 'components/mail/mail_accepted.html')
    except (TypeError, ValueError, OverflowError, IntegrityError, Task.DoesNotExist, TaskInvitation.DoesNotExist):
        return HttpResponse("Invalid invitation link", status=400)