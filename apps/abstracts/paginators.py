# DRF
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList

# Django
from django.core.paginator import Paginator


class AbstractPageNumberPaginator(PageNumberPagination):
    """AbstractPageNumberPaginator."""

    page_size_query_param: str = 'size'
    page_query_param: str = 'page'
    max_page_size: int = 10  # макс.кол объектов (игнор параметра в url)
    page_size: int = 2  # сколько объектов на страницу

    def get_paginated_response(
        self,
        data: ReturnList
    ) -> Response:
        response: Response = \
            Response(
                {
                    'pagination': {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link(),
                        'count': self.page.paginator.num_pages
                    },
                    'results': data
                }
            )
        return response


class AbstractLimitOffsetPagination(LimitOffsetPagination):
    """AbstractLimitOffsetPagination."""

    offset: int = 0
    limit: int = 2

    def get_paginated_response(
        self,
        data: ReturnList
    ) -> Response:
        response: Response = \
            Response(
                {
                    'pagination': {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link()
                    },
                    'results': data
                }
            )
        return response


class MyPagination:
    """My custom paginator."""

    count: int = 0
    num_pages: int = 0
    next_url: str = ''
    prev_url: str = ''

    def get_paginated_response(self, data):
        return Response(
            {
                'pagination': {
                    'count': self.count,
                    'num_pages': self.num_pages,
                    'next': self.next_url,
                    'prev': self.prev_url
                },
                'results': data
            }
        )

    def paginate_queryset(self, queryset, request):
        page: int
        try:
            page = int(request.GET['page'])
        except Exception:
            page = 1

        size: int
        try:
            size = int(request.GET['size'])
        except Exception:
            size = 10

        paginator = Paginator(queryset, size)

        self.count = paginator.count

        self.num_pages = paginator.num_pages

        url = request.build_absolute_uri()

        if page < self.num_pages:
            self.next_url = url.replace(
                "page="+str(page), "page=" + str(page+1)
            )
        else:
            self.next_url = ''

        if page > 1:
            self.prev_url = url.replace(
                "page="+str(page), "page=" + str(page-1)
            )
        else:
            self.prev_url = ''

        obj = paginator.page(page)

        return obj.object_list
