#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from .services import RepositoryDataService
from .views import get_commit_stats


class RepoCommitStats(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_invalid_request_type(self):
        request = self.factory.put(path='repo-stats/commit-stats')
        response = get_commit_stats(request)

        self.assertIsNotNone(response, "Response should not have a None value")
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class RepositoryDataServiceTestCase(APITestCase):

    def setUp(self):
        self.repository_data_service = RepositoryDataService()
        self.instance = "test_instance"
        self.repository_name = "test_repository_name"
        self.repository_id = "test_repository_id"
        self.token = "test_token"
        self.username = "test_username"
        self.from_date = "test_from_date"
        self.to_date = "test_to_date"

    @mock.patch("contribstats_apis.vsts.VSTSToken.get_credentials")
    @mock.patch("contribstats_apis.vsts.RepositoryStatsAPI.get_vsts_commit_stats")
    def test_fetch_commit_data_none_with_repository_name(self, mock_get_vsts_commit_stats, mock_get_credentials):

        mock_get_vsts_commit_stats.return_value = None
        mock_get_credentials.return_value = (self.username, self.token)

        data = self.repository_data_service.fetch_commit(project_name=self.repository_name, instance=self.instance,
                                                         from_date=self.from_date, to_date=self.to_date)

        self.assertIsNotNone(data, "Data value should not be None")
        self.assertEquals(data, {})

    @mock.patch("contribstats_apis.vsts.VSTSToken.get_credentials")
    @mock.patch("contribstats_apis.vsts.RepositoryStatsAPI.get_vsts_commit_stats")
    def test_fetch_commit_data_none_with_repository_id(self, mock_get_vsts_commit_stats, mock_get_credentials):

        mock_get_vsts_commit_stats.return_value = None
        mock_get_credentials.return_value = (self.username, self.token)

        data = self.repository_data_service.fetch_commit(project_name=None, project_id=self.repository_id, instance=self.instance,
                                                         from_date=self.from_date, to_date=self.to_date)

        self.assertIsNotNone(data, "Data value should not be None")
        self.assertEquals(data, {})

    @mock.patch("contribstats_apis.vsts.VSTSToken.get_credentials")
    @mock.patch("contribstats_apis.vsts.RepositoryStatsAPI.get_vsts_commit_stats")
    def test_fetch_commit_data_not_empty_with_empty_name(self, mock_get_vsts_commit_stats, mock_get_credentials):
        mock_get_vsts_commit_stats.return_value = "hello"
        mock_get_credentials.return_value = (self.username, self.token)

        data = self.repository_data_service.fetch_commit(project_name=None, project_id=self.repository_id,
                                                         instance=self.instance,
                                                         from_date=self.from_date, to_date=self.to_date)

        self.assertIsNotNone(data, "Data value should not be None")
        self.assertEquals(data, "hello")

    @mock.patch("contribstats_apis.vsts.VSTSToken.get_credentials")
    @mock.patch("contribstats_apis.vsts.RepositoryStatsAPI.get_vsts_commit_stats")
    def test_fetch_commit_data_not_empty_with_empty_id(self, mock_get_vsts_commit_stats, mock_get_credentials):
        mock_get_vsts_commit_stats.return_value = "hello"
        mock_get_credentials.return_value = (self.username, self.token)

        data = self.repository_data_service.fetch_commit(project_name=self.repository_name, project_id=None,
                                                         instance=self.instance,
                                                         from_date=self.from_date, to_date=self.to_date)

        self.assertIsNotNone(data, "Data value should not be None")
        self.assertEquals(data, "hello")
