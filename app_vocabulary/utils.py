from concurrent.futures import ThreadPoolExecutor

from app_translate.utils import translate, get_pronunciation
from app_vocabulary.models import EnglishVocabulary


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
