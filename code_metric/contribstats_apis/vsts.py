#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.cache import cache

import requests
import json


class VSTSToken:
    def __init__(self, username, personal_token):

        if username is None:
            pass

        if personal_token is None:
            pass

        self.username = username
        self.personal_token = personal_token


class VSTSProjectAPI:

    def __init__(self, instance='vsts-discovery', base_url='https://{}.VisualStudio.com/DefaultCollection/_apis/projects?api-version={}',
                 token='dcnnkkd4daub2nvs22ixpklskij4vohedmyfelwelnw2trueci5q', username='zcabmdo', api_version='1.0'):
        self.instance = instance
        self.api_version = api_version
        self.base_url = base_url.format(self.instance, self.api_version)
        self.username = username
        self.token = token


    def load_projects(self):
        """
        Load all projects from
        """
        r = requests.get(self.base_url, auth=(self.username, self.token))
        print('Retrieving projects from visual studio team services')

        if r.status_code != 200:
            print('Failed to fetch project data from Visual Studio Team Services={}'.format(r.text))
            return None

        else:

            data = r.json()

            print('Retrieved data: {}'.format(json.dumps(data)))

            print('Retrieved data: {} - count={}'.format(json.dumps(data), data['count']))
            for project in data['value']:
                print("Cache " + project['name'] + " - " + project['id'])
                # 1 hour TTL
                cache.set(project['name'], project['id'], 60*60)

            return data
