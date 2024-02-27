import timeit

import requests
from translators.server import GoogleV2, Bing


def stat_time(func):
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        end = timeit.default_timer()
        print(f'The execution time of function {func.__name__} was: {end - start}s')
        return result
    return wrapper


# @stat_time
def translate(query_text, from_language=None, to_language=None) -> str or None:
    if not from_language:
        from_language = 'en'
    if not to_language:
        to_language = 'vi'
    translated = google_translate(query_text, from_language, to_language)
    if not translated:
        translated = bing_translate(query_text, from_language, to_language)
    return translated


def google_translate(query_text: str, from_language: str, to_language: str) -> str or None:
    try:
        translator = GoogleV2()
        return translator.google_api(query_text=query_text, from_language=from_language, to_language=to_language)
    except Exception as exc:
        print(exc)


def bing_translate(query_text: str, from_language: str, to_language: str) -> str or None:
    try:
        translator = Bing()
        return translator.bing_api(query_text=query_text, from_language=from_language, to_language=to_language)
    except Exception as exc:
        print(exc)


# @stat_time
def get_pronunciation(query_text):
    endpoint = f"https://api.dictionaryapi.dev/api/v2/entries/en/{query_text}"
    response = requests.get(endpoint)
    if not response.status_code == 200:
        return [], []
    results = response.json()
    list_pronunciation, list_audio = set(), set()
    for result in results:
        phonetics = result.get('phonetics')
        if not phonetics:
            continue
        for phonetic in phonetics:
            pronunciation = phonetic.get('text')
            if pronunciation:
                list_pronunciation.update([pronunciation.replace('/', '')])
            audio = phonetic.get('audio')
            if audio:
                list_audio.update([audio])
    return list(list_pronunciation), list(list_audio)
