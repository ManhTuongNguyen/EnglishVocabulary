import os


def save_translated_word(word_id, word_en):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vocabulary.settings')

    import django
    django.setup()

    from app_translate.utils import translate, get_pronunciation
    from app_vocabulary.models import EnglishVocabulary

    text_translated = translate(query_text=word_en)
    list_pronunciation, list_audio = get_pronunciation(query_text=word_en)
    EnglishVocabulary.objects.filter(id=word_id).update(
        audio=', '.join(list_audio),
        translation=text_translated,
        pronunciation=', '.join(list_pronunciation)
    )
