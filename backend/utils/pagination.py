# backend/utils/pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except NotFound:
            self.page = None
            self.request = request
            return []

    def get_paginated_response(self, data):
        page_number = int(self.request.query_params.get(self.page_query_param, 1))

        return Response({
            "status": "success",
            "pagination": {
                "total_items": self.page.paginator.count if self.page else 0,
                "total_pages": self.page.paginator.num_pages if self.page else 1,
                "current_page": self.page.number if self.page else page_number,
                "next_page": self.get_next_link() if self.page else None,
                "previous_page": self.get_previous_link() if self.page else None,
                "page_size": self.get_page_size(self.request),
            },
            "results": data
        })
