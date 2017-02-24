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

    def test_retrieve_repo_id(self):
        repo_name = "minhlongdo/codemetric"

        repo_id = self.codeclimate_api.retrieve_repo_id(repo_name)

        self.assertIsNotNone(repo_id, 'Expect repo ID to be returned.')

    def test_get_codebase_gpa(self):
        repo_id = '58ada876fd025f027b002a92'

        codebase_gpa = self.codeclimate_api.get_codebase_gpa(repo_id)

        self.assertIsNotNone(codebase_gpa, 'Expect codebase gpa to be non zero')

    def test_get_test_history(self):
        repo_id = '58ada876fd025f027b002a92'

        test_coverage_history = self.codeclimate_api.get_codebase_test_coverage_history(repo_id)

        self.assertIsNotNone(test_coverage_history)
        self.assertTrue(len(test_coverage_history['data']) > 0)

    def test_get_test_history_empty(self):
        test_coverage_history = self.codeclimate_api.get_codebase_test_coverage_history(repo_id="test_id")

        self.assertIsNotNone(test_coverage_history)
        self.assertTrue(len(test_coverage_history['data']) == 0)

    def test_get_test_history_empty_id(self):
        self.assertRaises(ValueError, self.codeclimate_api.get_codebase_test_coverage_history, repo_id='')

    def test_get_test_history_none_id(self):
        self.assertRaises(ValueError, self.codeclimate_api.get_codebase_test_coverage_history, repo_id=None)
