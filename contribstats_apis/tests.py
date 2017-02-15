#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from .vsts import VSTSToken, VSTSGitAPI, RepositoryStatsAPI
from .exceptions import VSTSProjectException
from django.core.cache import cache
from datetime import datetime

import json


class VSTSTokenTest(TestCase):

    def test_initialize_username_with_token(self):
        vsts_token = VSTSToken(username='test_user', personal_token='test_token')
        self.assertIsNotNone(vsts_token, msg="Expect VSTS token object to be not None")

    def test_load_project_data_from_vsts(self):
        cache.clear()
        vsts_project_api = VSTSGitAPI()
        data = vsts_project_api.load_projects()
        self.assertIsNotNone(data)

        for project in data['value']:
            name = project['name']
            id = project['id']
            cached_id = cache.get(name)
            self.assertEqual(id, cached_id, "Expect to have cached the same ID")

    def test_get_project_name_that_exists(self):
        cache.clear()
        cache.set('test_name', 'test_id')

        project_id = VSTSGitAPI.get_id_for_name('test_name')
        self.assertEqual(project_id, 'test_id', "Expect the cache to have the key mapped to the id")

    def test_get_project_name_that_does_not_exist(self):
        cache.clear()

        self.assertRaises(VSTSProjectException, VSTSGitAPI.get_id_for_name, project_name='project_does_not_exist')


class TestRepositoryStatsAPI(TestCase):
    def setUp(self):
        self.repository_api = RepositoryStatsAPI()

    def test_construct_commit_stats_url_default(self):
        project_id = "test_repo_id"
        expected_string = "https://vsts-discovery.visualstudio.com/DefaultCollection/" \
                          "_apis/git/repositories/{}/commits?api-version=1.0&branch=master".format(project_id)

        self.assertEquals(expected_string, RepositoryStatsAPI.construct_commit_stats_url(project_id),
                          "Something is wrong with the default string construction")

    def test_parse_commit_stats_json(self):
        test_data = """{
  "count": 2,
  "value": [
    {
      "commitId": "27c01f18030287d33f57a935f156bf4add71b6f0",
      "author": {
        "name": "Minh-Long Do",
        "email": "minhlong.langos@gmail.com",
        "date": "2017-01-28T21:20:39Z"
      },
      "committer": {
        "name": "Minh-Long Do",
        "email": "minhlong.langos@gmail.com",
        "date": "2017-01-28T21:20:39Z"
      },
      "comment": "Fix django project.",
      "changeCounts": {
        "Add": 5,
        "Edit": 0,
        "Delete": 6
      },
      "url": "https://vsts-discovery.visualstudio.com/_apis/git/repositories/95bdbe6b-2f65-4190-99e4-238791b55b11/commits/27c01f18030287d33f57a935f156bf4add71b6f0",
      "remoteUrl": "https://vsts-discovery.visualstudio.com/_git/teacher-report/commit/27c01f18030287d33f57a935f156bf4add71b6f0"
    },
    {
      "commitId": "8255f409275ea902572dca07361626f7cdb6d3cf",
      "author": {
        "name": "Minh-Long Do",
        "email": "minhlong.langos@gmail.com",
        "date": "2017-01-28T21:02:10Z"
      },
      "committer": {
        "name": "Minh-Long Do",
        "email": "minhlong.langos@gmail.com",
        "date": "2017-01-28T21:02:10Z"
      },
      "comment": "Initial commit.",
      "changeCounts": {
        "Add": 9,
        "Edit": 0,
        "Delete": 0
      },
      "url": "https://vsts-discovery.visualstudio.com/_apis/git/repositories/95bdbe6b-2f65-4190-99e4-238791b55b11/commits/8255f409275ea902572dca07361626f7cdb6d3cf",
      "remoteUrl": "https://vsts-discovery.visualstudio.com/_git/teacher-report/commit/8255f409275ea902572dca07361626f7cdb6d3cf"
    }
  ]
}"""
        test_data_json = json.loads(test_data)
        expected_commit_ids = [
            '8255f409275ea902572dca07361626f7cdb6d3cf',
            '27c01f18030287d33f57a935f156bf4add71b6f0'
        ]
        commit_data = self.repository_api.parse_commit_data(test_data_json)

        epoch = datetime(day=28, month=1, year=2017).strftime("%s")

        print("Commit data: ", commit_data)
        print("Key value: ", commit_data[epoch])
        self.assertIsNotNone(commit_data)
        self.assertEquals(len(commit_data.keys()), 1)
        self.assertTrue(epoch in commit_data)
        self.assertEquals(len(commit_data[epoch]), 2)

        for commit in commit_data[epoch]:
            commit_id = commit['commit']['id']
            print("Commit Data: ", commit)
            print("Commit id: ", commit_id)
            # self.assertTrue(commit['id'] in expected_commit_ids)
            expected_commit_ids.remove(commit_id)

        self.assertEquals(len(expected_commit_ids), 0, "Expect commit id to be empty at the end")
