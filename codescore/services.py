#!/usr/bin/env python
# -*- coding: utf-8 -*-

from github.api import GitHubAPI
from codeclimate.api import CodeClimateAPI
from django.core.cache import cache


class CodeMetricService:
    def __init__(self, github_token, github_username='minhlongdo', github_base_url='https://api.github.com',
                 codeclimate_base_url='https://api.codeclimate.com/v1',
                 codeclimate_token='869a6e8e91bf5c32e7ccfc0f7d21392fc22beb27'):

        self.codeclimate_api = CodeClimateAPI(base_url=codeclimate_base_url, api_token=codeclimate_token)
        self.github_api = GitHubAPI(api_token=github_token, username=github_username, base_url=github_base_url)

    def map_github_with_codeclimate(self):
        github_repos = self.github_api.fetch_all_user_repos()

        self.codeclimate_api.retrieve_repo_metrics()