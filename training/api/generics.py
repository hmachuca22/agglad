# -*- coding: utf-8 -*-
from rest_framework.generics import ListAPIView
from .pagination import CustomPageNumberPagination


class CustomListAPIView(ListAPIView):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            paginate_response = self.request.query_params.get('paginate_response', 'false')
            if paginate_response in ['true', 'yes']:
                self._paginator = CustomPageNumberPagination()
            else:
                self._paginator = None

        return self._paginator
