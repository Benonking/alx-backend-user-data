#!/usr/bin/env python3
'''
manage api authnication
'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''
    Authentication class
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        define paths that do not need authentication
        '''
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # terate through the excluded_paths and check if path starts with any of them
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.rstrip('*')):
                return False

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
        retireve current validated user
        '''
        return None
