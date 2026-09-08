from rest_framework.pagination import PageNumberPagination

from apps.shared.utils.utils import success_response


class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return success_response(
            {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'has_next': self.page.has_next(),
                'results': data,
            }
        )
