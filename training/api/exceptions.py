# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

from . import errors


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now customize response...
    if response is not None:
        data = dict()
        data['code'] = exc.default_code.upper()
        data['message'] = exc.detail if isinstance(exc.detail, str) else exc.default_detail
        data['result'] = dict()
        if isinstance(exc.detail, (dict, list)):
            data['result']['errors'] = exc.detail

        response.data = data

    return response


class ResourceNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = errors.RESOURCES_NOT_FOUND
    default_detail = errors.RESOURCES_NOT_FOUND_MSG

    def __init__(self, **kwargs):
        super(ResourceNotFoundException, self).__init__(detail=kwargs.get('detail'), code=kwargs.get('code'))
