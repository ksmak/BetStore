# DRF
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    BasePagination,
)
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList


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


class MyPagination(BasePagination):
    """My custom paginator."""

    def get_paginated_response(self, data):
        return Response(
            {
                'pagination': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'results': data
            }
        )

    def paginate_queryset(self, queryset, request, view=None):
        pass
        # page_size = self.get_page_size(request)
        # if not page_size:
        #     return None

        # paginator = self.django_paginator_class(queryset, page_size)
        # page_number = self.get_page_number(request, paginator)

        # try:
        #     self.page = paginator.page(page_number)
        # except InvalidPage as exc:
        #     msg = self.invalid_page_message.format(
        #         page_number=page_number, message=str(exc)
        #     )
        #     raise NotFound(msg)

        # if paginator.num_pages > 1 and self.template is not None:
        #     # The browsable API should display pagination controls.
        #     self.display_page_controls = True

        # self.request = request
        # return list(self.page)