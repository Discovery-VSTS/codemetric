#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.exceptions import APIException


class InvalidRequest(APIException):
    status_code = 400
    default_detail = "Request data is None or empty"
    default_code = 'bad_request'


class RepositoryNotFound(APIException):
    status_code = 404
    default_detail = "Repository could not be found"
    default_code = 'not_found'


class UnexpectedError(APIException):
    status_code = 500
    default_detail = 'Something unexpected went wrong'
    default_code = 'internal_error'


class VSTSInstanceError(APIException):
    status_code = 400
    default_detail = 'Need instance value'
    default_code = 'bad_request'
