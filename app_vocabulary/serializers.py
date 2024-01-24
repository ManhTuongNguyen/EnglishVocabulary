import _thread

from rest_framework import serializers

from app_vocabulary.models import EnglishVocabulary
from app_vocabulary.utils import save_translated_word


class EnglishVocabularySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EnglishVocabulary
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        instance = super().create(validated_data)
        _thread.start_new_thread(save_translated_word, (instance.id, instance.word))
        return instance
