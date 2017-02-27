#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from contribstats_apis.exceptions import VSTSProjectException
from .services import RepositoryDataService
from .exceptions import InvalidRequest, RepositoryNotFound, UnexpectedError, VSTSInstanceError

repository_data_service = RepositoryDataService()


@api_view(['GET'])
def get_commit_stats(request):
    repo_name = request.GET.get('repo_name')
    branch = request.GET.get('branch')
    account = request.GET.get('account')

    if account is None:
        raise VSTSInstanceError

    print("Request data for repo={}".format(repo_name))
    print("Account={}".format(account))
    try:

        if branch is None:
            commit_data = repository_data_service.fetch_commit(project_name=repo_name, instance=account)
        else:
            commit_data = repository_data_service.fetch_commit(project_name=repo_name, branch=branch, instance=account)

        return Response(commit_data,
                        content_type="application/json",
                        status=status.HTTP_200_OK)

    except ValueError:
        raise InvalidRequest

    except VSTSInstanceError:
        raise VSTSInstanceError

    except VSTSProjectException:
        raise RepositoryNotFound

    except Exception:
        raise UnexpectedError
