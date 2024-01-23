from rest_framework import serializers

from app_vocabulary.models import EnglishVocabulary


class EnglishVocabularySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EnglishVocabulary
        exclude = ['created_at', 'updated_at']
