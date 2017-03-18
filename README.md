# Code Metric
[![Build Status](https://travis-ci.com/minhlongdo/codemetric.svg?token=2kqqx3kCC2fE4GJ6yBBG&branch=master)](https://travis-ci.com/minhlongdo/codemetric)

## Endpoints
- **repo-stats/commit-stats?instance_name=<instance_name>&repo_name=<repo_name>** To get the commit statistics from VSTS for a repository (source: VSTS)
- **code-score/gpa?instance_id=<instance_id>&user_email=<user_email>&github_repo=<github_repo>** To get codebase's GPA (source: Codeclimate)
- **code-score/test_coverage?instance_id=<instance_id>&github_repo=<github_repo>&user_email=<user_email>** To get test coverage history from repository (source: Codeclimate)