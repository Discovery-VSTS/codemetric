#!/usr/bin/env python
# -*- coding: utf-8 -*-


class VSTSProjectException(Exception):
    def __init__(self, project_name):
        super(VSTSProjectException, self).__init__(
            "Visual Studio Team Services project '{}' does not exist.".format(project_name))

        self.errors = "Project does not exist on Visual Studio Team Services"
