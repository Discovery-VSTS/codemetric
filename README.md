# Code Metric
[![Build Status](https://travis-ci.com/minhlongdo/codemetric.svg?token=2kqqx3kCC2fE4GJ6yBBG&branch=master)](https://travis-ci.com/minhlongdo/codemetric)

Zero start build
--------------------------

Create virtual environment with python 3.5+ as base interpreter

Run `pip install -r requirements.txt`

Finally, run `python manage.py runserver`

_Always make sure you are in the proper virtual environment_


Run
---

Just run `python manage.py runserver`

Documentation
-------------

This list can be accessed through `127.0.0.1:8000/docs`

Visit each link in the browser for a detailed description of each endpoint

## Brief Endpoints documentation
- **repo-stats/repos?instance_name=<instance_name>&instance_id=<instance_id>** Get all repos from team (source: VSTS)
- **repo-stats/commit-stats?instance_name=<instance_name>&repo_name=<repo_name>** To get the commit statistics from VSTS for a repository (source: VSTS)
- **code-score/gpa?instance_id=<instance_id>&user_email=<user_email>&github_repo=<github_repo>** To get codebase's GPA (source: Codeclimate)
- **code-score/test_coverage?instance_id=<instance_id>&github_repo=<github_repo>&user_email=<user_email>** To get test coverage history from repository (source: Codeclimate)
