#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from contribstats_apis.exceptions import VSTSProjectException
from .services import RepositoryDataService
from .exceptions import InvalidRequest, RepositoryNotFound, VSTSInstanceError

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
        logging.warn("Instance name is None or empty")
        raise VSTSInstanceError

    if repo_name is None or len(repo_name.strip()) <= 0:
        logging.warn("Repository name is None or empty")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:

        if branch is None:
            logging.info("Branch is none")
            commit_data = repository_data_service.fetch_commit(project_name=repo_name, instance=instance_name)
        else:
            logging.info('Branch={}'.format(branch))
            commit_data = repository_data_service.fetch_commit(project_name=repo_name, branch=branch,
                                                               instance=instance_name)

        return JsonResponse(commit_data)

    except ValueError as e:
        logging.warn(e)
        raise InvalidRequest

    except VSTSInstanceError:
        raise VSTSInstanceError

    except VSTSProjectException:
        raise RepositoryNotFound

    except Exception as e:
        logging.error(e)
        return Response(data=e, status=HTTP_500_INTERNAL_SERVER_ERROR)
