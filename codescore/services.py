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

    def map_github_with_codeclimate_in_cache(self):
        github_repos = self.github_api.fetch_all_user_repos()

        for github_repo in github_repos:
            repo_name = github_repo['full_name']
            repo_id = self.codeclimate_api.retrieve_repo_id(repo_name)

            cache.set(repo_name, repo_id, 60 * 60)

    def retrieve_repo_id_using_repo_name(self, repo_name):
        repo_id = cache.get(repo_name)

        if repo_id is None:
            repo_id = self.codeclimate_api.retrieve_repo_id(repo_name=repo_name)
            if repo_id is None:
                return None
            else:
                cache.set(repo_name, repo_id, 60 * 60)
                return repo_id

        return repo_id
