from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=50, blank=True)
    skill_level = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username