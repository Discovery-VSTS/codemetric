#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import get_commit_stats


urlpatterns = [
    url(r'^commit-stats/$', view=get_commit_stats, name='commit-stats')
]
