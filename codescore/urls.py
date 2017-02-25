#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import get_codebase_gpa, get_test_coverage_history

urlpatterns = [
    url(r'gpa/(?P<github_user>\w{0,50})/(?P<github_repo>\w{0,50})/$', view=get_codebase_gpa),
    url(r'test_coverage/(?P<github_user>\w{0,50})/(?P<github_repo>\w{0,50})/$', view=get_test_coverage_history)
]
