#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from .vsts import VSTSToken, VSTSProjectAPI
from django.core.cache import cache


class VSTSTokenTest(TestCase):

    def test_initialize_username_with_token(self):
        vsts_token = VSTSToken(username='test_user', personal_token='test_token')
        self.assertIsNotNone(vsts_token, msg="Expect VSTS token object to be not None")

    def test_load_project_data_from_vsts(self):
        vsts_project_api = VSTSProjectAPI()
        data = vsts_project_api.load_projects()
        self.assertIsNotNone(data)

        for project in data['value']:
            name = project['name']
            id = project['id']
            cached_id = cache.get(name)
            self.assertEqual(id, cached_id, "Expect to have cached the same ID")
