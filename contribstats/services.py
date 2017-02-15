#!/usr/bin/env python
# -*- coding: utf-8 -*-
from contribstats_apis.vsts import RepositoryStatsAPI, VSTSGitAPI, VSTSToken


class RepositoryDataService:
    def __init__(self):
        self.repository_stats_api = RepositoryStatsAPI()
        self.git_api = VSTSGitAPI()
        self.vsts_token = VSTSToken()

    def change_user(self, username):
        self.vsts_token.set_user(username=username)

    def change_pass(self, token):
        self.vsts_token.set_token(token=token)

    def fetch_commit(self, project_name, project_id=None, instance='vsts-discovery', from_date=None, to_date=None):
        username, token = self.vsts_token.get_credentials()
        print("going to fetch commit")
        print("project name={}".format(project_name))
        data = self.repository_stats_api.get_vsts_commit_stats(instance=instance,
                                                               project_name=project_name,
                                                               project_id=project_id,
                                                               token=token, username=username,
                                                               from_date=from_date, to_date=to_date)

        print("Retrieve data={}".format(data))

        if data is None:
            return {}
        else:
            return data
