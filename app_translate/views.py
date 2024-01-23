from concurrent.futures import ThreadPoolExecutor

from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import serializers, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from app_translate.utils import translate, get_pronunciation


@extend_schema(tags=['Translate'], operation_id='translate')
class Translate(APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    @extend_schema(
        request=inline_serializer(
            name='Translation',
            fields={
                'query_text': serializers.CharField(
                    help_text='Text want to translate',
                    required=True
                ),
                'is_include_pronunciation': serializers.BooleanField(
                    help_text='Is include pronunciation',
                    required=False,
                    default=False
                ),
                'from_language': serializers.CharField(
                    help_text='From language want to translate',
                    default='en',
                    required=False
                ),
                'to_language': serializers.CharField(
                    help_text='To language want to translate',
                    default='vi',
                    required=False
                ),
            }
        ),
        responses={
            200: inline_serializer(
                name='Translation of Translation',
                fields={
                    'query_text': serializers.CharField(
                        help_text='Text want to translate'
                    ),
                    'text_translated': serializers.CharField(
                        help_text='Text translated'
                    ),
                }
            ),
            400: OpenApiResponse(),
        },
        description='Translate language'
    )
    def post(request):
        query_text = request.data.get('query_text')
        from_language = request.data.get('from_language')
        to_language = request.data.get('to_language')
        is_include_pronunciation = request.data.get('is_include_pronunciation', False)
        if isinstance(is_include_pronunciation, str):
            is_include_pronunciation = is_include_pronunciation.lower() == 'true'

        if not query_text:
            return Response({'message': 'query_text is required'}, status=400)

        list_pronunciation, list_audio = [], []
        with ThreadPoolExecutor() as executor:
            # get translation word
            future1 = executor.submit(translate, query_text=query_text, from_language=from_language,
                                      to_language=to_language)

            # get pronunciation
            if is_include_pronunciation:
                future2 = executor.submit(get_pronunciation, query_text=query_text)
                list_pronunciation, list_audio = future2.result()
            text_translated = future1.result()
        result = {
            'query_text': query_text,
            'text_translated': text_translated,
        }
        if is_include_pronunciation:
            result.update({
                'list_pronunciation': list_pronunciation,
                'list_audio': list_audio,
            })
        return Response(result)
