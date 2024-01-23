from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from openpyxl import Workbook
from openpyxl.styles import Font
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from app_api_gateway.utils import CustomPagination
from app_vocabulary.models import EnglishVocabulary
from app_vocabulary.serializers import EnglishVocabularySerializer


@extend_schema(tags=['Vocabulary'], operation_id='vocabulary')
class EnglishVocabularyViewSet(ModelViewSet):
    serializer_class = EnglishVocabularySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return EnglishVocabulary.objects.filter(user=self.request.user)

    @action(methods=['get'], detail=False, url_path='download-workbook')
    def get_workbook(self, request):
        # Create a Workbook
        workbook = Workbook()
        worksheet = workbook.active

        # Define headers
        headers = ['STT', 'Word', 'Translation', 'Pronunciation', 'Link audio']

        queryset = EnglishVocabulary.objects.all().values_list('word', 'translation', 'pronunciation', 'audio')

        # Write headers to the first row
        header_style = Font(bold=True)
        for col_num, header in enumerate(headers, 1):
            col_letter = worksheet.cell(row=1, column=col_num)
            col_letter.value = header
            col_letter.font = header_style

        # Write data to the following rows
        for row_num, obj in enumerate(queryset, 2):
            row = [
                row_num - 1,
                obj[0],
                obj[1],
                obj[2],
                ', '.join(obj[3]),
            ]
            worksheet.append(row)

        # Create an HTTP response with the excel to download
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=word_{request.user.username}.xlsx'
        workbook.save(response)

        return response
