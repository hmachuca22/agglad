# -*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_page_size(self, request):
        return request.GET.get(self.page_size_query_param, 6)

    def get_paginated_response(self, data):
        return Response(
            dict(
                links=dict(
                    next=self.get_next_link(),
                    previous=self.get_previous_link()
                ),
                page=dict(
                    next=self.page.next_page_number() if self.page.has_next() else None,
                    current=self.page.number,
                    previous=self.page.previous_page_number() if self.page.has_previous() else None
                ),
                count=self.page.paginator.count,
                results=data
            )
        )
