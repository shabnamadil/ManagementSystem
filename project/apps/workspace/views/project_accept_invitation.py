from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.db import IntegrityError
from django.shortcuts import render

from ..models import (
    ProjectMember,
    WorkspaceProject,
    ProjectMemberInvitation
)


User = get_user_model()


def project_accept_invitation(request, uid, email, token):
    try:
        project_id = urlsafe_base64_decode(uid).decode()
        decoded_email = urlsafe_base64_decode(email).decode()
        project = get_object_or_404(WorkspaceProject, id=project_id)
        invitation = get_object_or_404(ProjectMemberInvitation, project=project, token=token)

        # Add the user to the workspace members (assuming user is authenticated)
        user = User.objects.get(email=decoded_email) # or use the email to find the user
        project_member = ProjectMember.objects.create(project=project, role='Adi üzv', user=user)
        project_member.save()

        # Delete the invitation or mark it as accepted
        invitation.is_accepted = True
        invitation.save()

        # return redirect('project-detail', pk=project.id)  # Redirect to the project page
        return render(request, 'components/mail/mail_accepted.html')
    except (TypeError, ValueError, OverflowError, IntegrityError, WorkspaceProject.DoesNotExist, ProjectMemberInvitation.DoesNotExist):
        return HttpResponse("Invalid invitation link", status=400)