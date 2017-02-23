#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from .api import GitHubAPI
from unittest import skip


class GithubAPITest(TestCase):
    def setUp(self):
        self.github_api = GitHubAPI()

    @skip(reason="If this is run on travis, the personal token will be automatically deleted")
    def test_get_user_repos(self):
        data = self.github_api.fetch_all_user_repos()

        self.assertIsNotNone(data)
        self.assertTrue(len(data) > 0)
