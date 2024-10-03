from django.db import models
from django.contrib.auth import get_user_model

from utils.models.base_model import BaseModel
from utils.manager.published_comment import PublishedBlogCommentManager
from .blog_item import Blog

User = get_user_model()


class BlogComment(BaseModel):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    comment_text = models.TextField(
        'Bloq rəyi'
    )
    blog = models.ForeignKey(
        Blog, 
        on_delete=models.CASCADE, 
        related_name='blog_comments',
        verbose_name='Bloq'
    )
    comment_author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blog_comments',
        verbose_name='Rəy müəllifi'
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PUBLISHED
    )
    objects = models.Manager()
    published = PublishedBlogCommentManager()

    class Meta:
          verbose_name = ('Bloq rəyi')
          verbose_name_plural = ('Bloq rəyləri')
          ordering = ['-created']
          indexes = [
            models.Index(fields=['-created'])
        ]
            
    @property
    def truncated_comment(self):
        max_words = 3
        words = self.comment_text.split()
        truncated_words = words[:max_words]
        truncated_content = ' '.join(truncated_words)

        if len(words) > max_words:
            truncated_content += ' ...'  

        return truncated_content

    def __str__(self) -> str:
        return self.truncated_comment