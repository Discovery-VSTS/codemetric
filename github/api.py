#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class GitHubAPI:
    def __init__(self, api_token, username='minhlongdo',
                 base_url='https://api.github.com'):
        self.username = username
        self.api_token = api_token
        self.base_url = base_url

    def set_username(self, username):
        self.username = username

    def set_api_token(self, api_token):
        self.api_token = api_token

    def fetch_all_user_repos(self):
        request_url = self.base_url + "/users/{}/repos".format(self.username)

        headers = {
            'Accept': 'application/vnd.github.inertia-preview+json'
        }

        try:
            r = requests.get(request_url, headers=headers, auth=(self.username, self.api_token))

            print("Received data: ", r)

            if r.status_code == 200:
                print("Received data: ", r.json())
                return r.json()

            r.raise_for_status()
        except Exception as e:
            print("Something unexpected happened")
            raise Exception(e)
