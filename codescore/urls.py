#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import get_codebase_gpa, get_test_coverage_history, hello_world

urlpatterns = [
    url(r'gpa/$', view=get_codebase_gpa),
    url(r'test_coverage/$', view=get_test_coverage_history),
    url(r'hello_world/$', view=hello_world)
]
