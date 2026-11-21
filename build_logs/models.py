from django.conf import settings
from django.db import models

from projects.models import Project


class BuildLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='logs')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='build_logs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Project: {self.project.name} - "{self.title}"'