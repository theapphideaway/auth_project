from rest_framework import serializers
from .models import UserProfile, SavedWord


class SavedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedWord
        fields = ['id', 'origin', 'english_translation', 'origin_language']


class UserProfileSerializer(serializers.ModelSerializer):
    saved_words = SavedWordSerializer(many=True, read_only=True)  # Include saved words

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'preferred_language', 'skill_level', 'saved_words']

