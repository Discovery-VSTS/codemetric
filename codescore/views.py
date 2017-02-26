#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import CodeMetricService
from .exceptions import RepoIDNotFound

import json


@api_view(['GET'])
def get_codebase_gpa(request, github_user, github_repo):
    github_api_token = request.META['HTTP_AUTHORIZATION']

    if github_api_token is None or len(github_api_token) <= 0:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        codemetric_service = CodeMetricService(github_token=github_api_token)

        repo_id = codemetric_service.retrieve_repo_id_using_repo_name(github_user + "/" + github_repo)

        data = {
            'user': github_user,
            'repo_name': github_repo,
            'repo_id': repo_id,
        }

        if repo_id is None or len(repo_id) <= 0:
            data['gpa'] = '-1'
            return Response(data=json.dumps(data),
                            status=status.HTTP_404_NOT_FOUND,
                            content_type="application/json")

        codebase_gpa = codemetric_service.get_codebase_gpa(repo_id)

        data['gpa'] = codebase_gpa

        return Response(data=json.dumps(data),
                        content_type="application/json",
                        status=status.HTTP_200_OK)

    except ValueError as e:
        print("Empty repo ID or None Value: ", e)
        raise RepoIDNotFound

    except Exception as e:
        print("Something went wrong - ", e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_test_coverage_history(request, github_user, github_repo):
    github_api_token = request.META['HTTP_AUTHORIZATION']

    if github_api_token is None or len(github_api_token) <= 0:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        codemetric_service = CodeMetricService(github_token=github_api_token)

        repo_id = codemetric_service.retrieve_repo_id_using_repo_name(repo_name=github_user + "/" + github_repo)

        data = {
            'user': github_user,
            'repo_name': github_repo,
            'repo_id': repo_id,
        }

        test_coverage_history = codemetric_service.get_test_coverage_history(repo_id=repo_id)

        if test_coverage_history is None or len(test_coverage_history) <= 0:
            data['coverage-history'] = []
            return Response(data=json.dumps(data),
                            status=status.HTTP_200_OK,
                            content_type="application/json")

        data['coverage-history'] = test_coverage_history
        return Response(data=json.dumps(data),
                        status=status.HTTP_200_OK,
                        content_type="application/json")

    except ValueError as e:
        print("Empty repo ID or None Value: ", e)
        raise RepoIDNotFound

    except Exception as e:
        print("Something unexpected happened")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def hello_world(request):
    return Response(data="hello", content_type="text/plain")
