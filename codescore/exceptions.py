#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.exceptions import APIException


class RepoIDNotFound(APIException):
    status_code = 404
    default_detail = 'Repo ID does not exist'
    default_code = 'not_found'
