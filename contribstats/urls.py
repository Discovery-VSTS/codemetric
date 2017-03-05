#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import get_commit_stats


urlpatterns = [
    url('commit-stats/(?P<instance_name>\w{0,50})/(?P<repo_name>\w{0,50})/$', view=get_commit_stats, name='commit-stats')
]
