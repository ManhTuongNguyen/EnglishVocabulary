import multiprocessing

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
        process = multiprocessing.Process(target=save_translated_word, args=(instance.id, instance.word))
        process.start()
        return instance
