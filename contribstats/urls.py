#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import get_commit_stats, get_all_repos


urlpatterns = [
    url(r'^commit-stats/$', view=get_commit_stats, name='commit-stats'),
    url(r'^repos/$', view=get_all_repos, name='all-repos')
]
