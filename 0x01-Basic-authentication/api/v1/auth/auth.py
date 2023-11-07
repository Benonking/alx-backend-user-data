#!/usr/bin/env python3
'''
manage api authnication
'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        define paths that do not need authentication
        '''
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Ensure that path ends with a trailing slash
        if not path.endswith('/'):
            path += '/'

        # Check if path is in the list of excluded_paths
        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        '''
        Validate authorization
        '''
        if request is None:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        '''
        return None
