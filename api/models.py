from django.contrib.auth.models import User
from django.db import models


class SavedWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    english_translation = models.CharField(max_length=100)
    origin_language = models.CharField(max_length=50)

    def __str__(self):
        return self.origin


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=50, blank=True)
    skill_level = models.CharField(max_length=20, blank=True)
    saved_words = models.ManyToManyField(SavedWord, blank=True)

    def __str__(self):
        return self.user.username


