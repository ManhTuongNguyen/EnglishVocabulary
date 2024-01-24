from django.db import connection, transaction

from app_translate.utils import translate, get_pronunciation


def save_translated_word(word_id, word_en):
    text_translated = translate(query_text=word_en)
    list_pronunciation, list_audio = get_pronunciation(query_text=word_en)
    cursor = connection.cursor()
    query = f"""
            UPDATE tb_vocabulary 
            SET audio = '{', '.join(list_audio)}',
            translation = '{text_translated}',
            pronunciation = '{', '.join(list_pronunciation)}'
            WHERE id = '{str(word_id).replace("-", "")}';
            """
    cursor.execute(query)
    transaction.commit()
    print("Update query executed successfully!")
