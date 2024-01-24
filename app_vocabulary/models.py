import uuid

from django.contrib.auth.models import User
from django.db import models


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
