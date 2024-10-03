from django.db import models
from apps.blog import models as mod


class PublishedBlogCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=mod.BlogComment.Status.PUBLISHED)