from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User

class Url(models.Model):
    longurl = models.URLField(max_length=300)
    shorturl = models.CharField(max_length=5, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.longurl
