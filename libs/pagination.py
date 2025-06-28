from rest_framework.pagination import PageNumberPagination
from libs.response import APIResponse

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class to handle paginated responses.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return APIResponse.success(
            message="Paginated results fetched successfully",
            data={
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            }
        )
