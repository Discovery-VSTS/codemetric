#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class CodeClimateAPI:
    def __init__(self, api_token="869a6e8e91bf5c32e7ccfc0f7d21392fc22beb27",
                 base_url='https://api.codeclimate.com/v1'):
        self.api_token = api_token
        self.base_url = base_url

    def set_api_token(self, api_token):
        self.api_token = api_token

    def set_base_url(self, base_url):
        self.base_url = base_url

    def retrieve_repo_id(self, repo_name="minhlongdo/codemetric"):
        request_url = self.base_url + "/repos"
        headers = {
            'Authorization': 'Token {}'.format(self.api_token),
            'Accept': 'application/vnd.api+json'
        }
        params = {
            'github_slug': repo_name
        }

        try:
            r = requests.get(request_url, headers=headers, params=params)

            if r.status_code == 200:
                for entry in r.json()['data']:
                    if entry['attributes']['github_slug'] == repo_name:
                        return entry['id']

            return None

        except Exception as e:
            print("Something unexpected happened")
            raise Exception(e)

    def get_codebase_gpa(self, repo_id):
        if repo_id is None or len(repo_id) == 0:
            raise ValueError("Repository name cannot be None or empty")

        request_url = self.base_url + "/repos/{}".format(repo_id)
        headers = {
            'Authorization': 'Token {}'.format(self.api_token),
            'Accept': 'application/vnd.api+json'
        }

        try:
            r = requests.get(request_url, headers=headers)

            if r.status_code == 200:
                codebase_gpa = r.json()['data']['attributes']['score']
                print("Codebase GPA: {}".format(codebase_gpa))
                return codebase_gpa

            return None

        except Exception as e:
            print("Something unexpected happened")
            raise Exception(e)

    def get_codebase_test_coverage(self, repo_name):
        pass
