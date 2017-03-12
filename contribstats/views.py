#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from contribstats_apis.exceptions import VSTSProjectException
from .services import RepositoryDataService
from .exceptions import InvalidRequest, RepositoryNotFound, UnexpectedError, VSTSInstanceError

import logging

repository_data_service = RepositoryDataService()


@api_view(['GET'])
def get_commit_stats(request):
    """
    Get commit statistics from VSTS git repository. Default branch is going to be 'master'.
    """
    logging.info('Get commit stats')
    instance_name = request.GET.get('instance_name')
    repo_name = request.GET.get('repo_name')
    branch = request.GET.get('branch')

    if instance_name is None or len(instance_name.strip()) <= 0:
        raise VSTSInstanceError

    if repo_name is None or len(repo_name.strip()) <= 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    print("Request data for repo={}".format(repo_name))

    try:

        if branch is None:
            commit_data = repository_data_service.fetch_commit(project_name=repo_name, instance=instance_name)
        else:
            commit_data = repository_data_service.fetch_commit(project_name=repo_name, branch=branch,
                                                               instance=instance_name)

        return Response(commit_data,
                        content_type="application/json",
                        status=status.HTTP_200_OK)

    except ValueError as e:
        logging.warn(e)
        raise InvalidRequest

    except VSTSInstanceError:
        raise VSTSInstanceError

    except VSTSProjectException:
        raise RepositoryNotFound

    except Exception as e:
        logging.error(e)
        raise UnexpectedError
