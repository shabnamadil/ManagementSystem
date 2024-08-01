from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.models.base_model import BaseModel
from utils.slugify.custom_slugify import custom_slugify

User = get_user_model()

class WorkspaceCategory(BaseModel):
    BG_COLOR_PALETTE = [
        ("bg-danger", "red", ),
        ("bg-primary", "blue", ),
        ("bg-success", "green", ),
        ("bg-warning", "yellow", ),
        ("bg-light", "white", ),
        ("bg-dark", "black", ),
    ]
    TEXT_COLOR_PALETTE = [
        ("text-danger", "red", ),
        ("text-primary", "blue", ),
        ("text-success", "green", ),
        ("text-warning", "yellow", ),
        ("text-light", "white", ),
        ("text-dark", "black", ),
    ]
    title = models.CharField(max_length = 200)
    text_color = models.CharField(max_length = 50, choices = TEXT_COLOR_PALETTE, null = True, blank = True)
    bg_color = models.CharField(max_length = 50, choices = BG_COLOR_PALETTE, null = True, blank = True)
    
    def __str__(self) -> str:
        return self.title

class Workspace(BaseModel):
    title = models.CharField(max_length = 200, unique = True)
    slug = models.SlugField(blank=True, null=True, unique = True)
    description = models.TextField(null = True, blank = True)
    categories = models.ManyToManyField(WorkspaceCategory, related_name = 'workspaces')
    # image = models.ImageField(upload_to = 'workspaces', null = True, blank = True)
    # notifications = models.IntegerField(choices = NOTIFICATIONS, null = True, blank = True)

    def save(self, *args, **kwargs):
        self.slug = custom_slugify(self.title)
        super(Workspace, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    # def get_absolute_url(self):
    #     return reverse("workspace-detail", kwargs={"slug": self.slug})

class WorkspaceUser(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'workspace_users')
    workspace = models.ForeignKey(Workspace, on_delete = models.CASCADE, related_name = 'workspace_users')
    is_creator = models.BooleanField(default = False)
    is_moderator = models.BooleanField(default = False)

    class Meta:
        unique_together = ['user', 'workspace']

    def __str__(self) -> str:
        return f'{self.user}'