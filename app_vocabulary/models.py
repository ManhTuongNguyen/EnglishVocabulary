import _thread
import uuid
from concurrent.futures import ThreadPoolExecutor

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from app_translate.utils import translate, get_pronunciation


class EnglishVocabulary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.CharField(max_length=50, unique=True)
    translation = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    pronunciation = models.CharField(max_length=150, null=True, blank=True)
    audio = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tb_vocabulary'
        verbose_name = 'Vocabulary'
        verbose_name_plural = 'List vocabulary'


@receiver(post_save, sender=EnglishVocabulary)
def create_user_profile(**kwargs):
    instance = kwargs.get('instance', None)
    _thread.start_new_thread(save_translated_word, (instance.id, instance.word))


def save_translated_word(word_id, word_en):
    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(translate, query_text=word_en)
        future2 = executor.submit(get_pronunciation, query_text=word_en)
        text_translated = future1.result()
        list_pronunciation, list_audio = future2.result()
    EnglishVocabulary.objects.filter(id=word_id).update(
        translation=text_translated,
        pronunciation=', '.join(list_pronunciation),
        audio=list_audio
    )
