from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 999999

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get('all'):
            self.page_size = len(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_next_link(self):
        if self.page.paginator.count == self.page_size:
            return None
        return super().get_next_link()

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total_object', self.page.paginator.count),
            ('current_page', self.page.number),
            ('total_page', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
