
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.db import transaction
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from apps.workspace.models import (
    Workspace,
    Task
)

User = get_user_model()


# def set_super_admin(instance, user):
#     if instance.admins.exists():
#         instance.super_admin = instance.admins.all()[0]
#     else:
#         instance.super_admin = None
#     instance.save()

# def set_admin(instance, user):
#     if user in instance.admins.all():
#         instance.admins.remove(user)
#     if not instance.admins.exists() and instance.members.exists():
#         instance.admins.add(instance.members.all()[0])
#     instance.save()


# @receiver(post_save, sender=Workspace)
# def add_workspace_creator_to_members_admins_super_admin(sender, instance, created, **kwargs):
#     if created:
#         transaction.on_commit(lambda: instance.members.add(instance.creator))
#         transaction.on_commit(lambda: instance.admins.add(instance.creator))
#         transaction.on_commit(lambda: Workspace.objects.filter(pk=instance.pk).update(super_admin=instance.creator))


# @receiver(m2m_changed, sender=Workspace.members.through)
# def change_admin(sender, instance, action, reverse, pk_set, **kwargs):
#     if action == 'post_remove':
#         with transaction.atomic():
#             for user_id in pk_set:
#                 try:
#                     user = User.objects.get(pk=user_id)
#                     transaction.on_commit(lambda: set_admin(instance, user))
#                 except User.DoesNotExist:
#                     continue
#             instance.save()


# @receiver(m2m_changed, sender=Workspace.members.through)
# def change_super_admin(sender, instance, action, reverse, pk_set, **kwargs):
#     if action == 'post_remove':
#         with transaction.atomic():
#             for user_id in pk_set:
#                 try:
#                     user = User.objects.get(pk=user_id)
#                     if user == instance.super_admin:
#                         transaction.on_commit(lambda: set_super_admin(instance, user))
#                 except User.DoesNotExist:
#                     continue
#             instance.save()