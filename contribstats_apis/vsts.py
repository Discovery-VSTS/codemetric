#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.cache import cache
from requests.exceptions import HTTPError
from datetime import datetime
from .exceptions import VSTSProjectException

import requests
import json


class VSTSToken:
    def __init__(self, username='zcabmdo',
                 personal_token='dcnnkkd4daub2nvs22ixpklskij4vohedmyfelwelnw2trueci5q'):

        self.username = username
        self.personal_token = personal_token

    def get_credentials(self):
        return self.username, self.personal_token

    def set_user(self, username):
        self.username = username

    def set_token(self, token):
        self.personal_token = token


class VSTSGitAPI:

    def __init__(self, instance='vsts-discovery', base_url='https://{}.VisualStudio.com/DefaultCollection/_apis/git/repositories?api-version={}',
                 token='dcnnkkd4daub2nvs22ixpklskij4vohedmyfelwelnw2trueci5q', username='zcabmdo', api_version='1.0'):
        self.instance = instance
        self.api_version = api_version
        self.base_url = base_url
        self.username = username
        self.token = token

    def load_projects(self):
        """
        Load all projects from
        """

        data = VSTSGitAPI.fetch__all_git_repo_id(instance=self.instance,
                                                 base_url=self.base_url,
                                                 username=self.username,
                                                 token=self.token,
                                                 api_version=self.api_version)

        return data

    @staticmethod
    def fetch__all_git_repo_id(instance='vsts-discovery',
                               base_url='https://{}.VisualStudio.com/DefaultCollection/'
                                        '_apis/git/repositories?api-version={}',
                               token='dcnnkkd4daub2nvs22ixpklskij4vohedmyfelwelnw2trueci5q',
                               username='zcabmdo', api_version='1.0'):
        """
        Send request to fetch all repository name with its associated id from VSTS
        """
        try:
            request_url = base_url.format(instance, api_version)
            r = requests.get(request_url, auth=(username, token))

            r.raise_for_status()

            if r.status_code != 200:
                print("Failed to fetch repository id from VSTS")
                return {}
            else:

                data = r.json()
                print("Retrieved data={} - count={}".format(json.dumps(data), data['count']))

                for repo in data['value']:
                    cache.set(repo['name'], repo['id'])

                return data

        except Exception as e:
            print("Something unexpected happened: ", e)
            raise Exception("Something unexpected happened")

    @staticmethod
    def get_id_for_name(project_name,
                        instance='vsts-discovery',
                        base_url='https://{}.VisualStudio.com/DefaultCollection/_apis/git/repositories?api-version={}',
                        token='dcnnkkd4daub2nvs22ixpklskij4vohedmyfelwelnw2trueci5q',
                        username='zcabmdo',
                        api_version='1.0'):
        base_url = base_url.format(instance, api_version)
        print("Getting project_name={} from Memcached".format(project_name))

        project_id = cache.get(project_name)
        if project_id is None:

            try:
                # Need to request server for more project names
                r = requests.get(base_url, auth=(username, token))
                r.raise_for_status()

                # Parse project json data
                data = r.json()

                print('Retrieved data: {}'.format(json.dumps(data)))

                print('Retrieved data: {} - count={}'.format(json.dumps(data), data['count']))
                for project in data['value']:
                    print("Cache " + project['name'] + " - " + project['id'])
                    # 1 hour TTL
                    cache.set(project['name'], project['id'], 60 * 60)

                project_id = cache.get(project_name)

                if project_id is None:
                    print("Project name '{}' does not exist".format(project_name))
                    raise VSTSProjectException(project_name)

                return project_id

            except HTTPError as e:
                print('Failed to fetch project data from Visual Studio Team Services={}'.format(e))
                raise HTTPError(e)

        else:
            print("Key '{}' is cached and its value is '{}'".format(project_name, project_id))
            return project_id


class RepositoryStatsAPI:
    def __init__(self):
        pass

    @staticmethod
    def construct_commit_stats_url(project_id, instance='vsts-discovery', branch='master',
                                   from_date=None, to_date=None, api_version='1.0'):
        """
        By default it will look only for stats in the master branch.
        """
        base_url = "https://{}.visualstudio.com/DefaultCollection/_apis/git/" \
                   "repositories/{}/commits?" \
                   "api-version={}&branch={}".format(instance, project_id, api_version, branch)

        if from_date is not None:
            base_url += "&fromDate={}".format(from_date)

        if to_date is not None:
            base_url += "&toDate={}".format(to_date)

        print("Constructed base url={}".format(base_url))
        return base_url

    @staticmethod
    def parse_commit_data(data):
        """
        Sort commits into dates and contributors
        """
        print("Repository commit stats data: ", data)
        if data is None:
            raise ValueError('data cannot be None')

        commit_data = {}
        for commit in data['value']:
            date = datetime.strptime(commit['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
            epoch = datetime(day=date.day, month=date.month, year=date.year).strftime("%s")

            commit_data_entry = {
                epoch: {
                    'commit': {
                        'id': commit['commitId'],
                        'author': {
                            'name': commit['committer']['name'],
                            'email': commit['committer']['email']
                        },
                        'changes': {
                            'add': commit['changeCounts']['Add'],
                            'delete': commit['changeCounts']['Delete'],
                            'edit': commit['changeCounts']['Edit']
                        }
                    }
                }
            }

            print("Commit data in function: ", commit_data)

            if commit_data is None:
                commit_data = [commit_data_entry]
            else:
                if epoch in commit_data.keys():
                    commit_data[epoch].append(commit_data_entry[epoch])
                else:
                    commit_data[epoch] = [commit_data_entry[epoch]]
        return commit_data

    def get_vsts_commit_stats(self, instance='vsts-discovery', project_name=None, project_id=None,
                              from_date=None, to_date=None,
                              token='dcnnkkd4daub2nvs22ixpklskij4vohedmyfelwelnw2trueci5q', username='zcabmdo'):
        try:
            vsts_project_id = VSTSGitAPI.get_id_for_name(project_name=project_name)

            print("Project name {} id is {}".format(project_name, vsts_project_id))

            # Construct request url to get commit data from repository
            request_url = RepositoryStatsAPI.construct_commit_stats_url(project_id=vsts_project_id,
                                                                        instance=instance,
                                                                        from_date=from_date,
                                                                        to_date=to_date)

            # Send request to VSTS server to get repository commit data
            r = requests.get(request_url, auth=(username, token))
            r.raise_for_status()

            # Start doing request using project's ID
            commit_data = RepositoryStatsAPI.parse_commit_data(r.json())
            # return as a JSON
            return commit_data

        except ValueError:
            print("Project Name and project ID cannot both be None")
            raise ValueError("Project name and project ID cannot both be None")

        except VSTSProjectException:
            raise VSTSProjectException(project_name)

        except HTTPError as e:
            raise HTTPError(e)

        except Exception as e:
            raise RuntimeError("Something unexpected happened: {}".format(e))
