#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from .api import CodeClimateAPI


class CodeClimateAPITest(TestCase):
    def setUp(self):
        self.codeclimate_api = CodeClimateAPI()

    def test_get_repo_gpa(self):
        self.assertRaises(ValueError,
                          self.codeclimate_api.get_codebase_gpa, None)
