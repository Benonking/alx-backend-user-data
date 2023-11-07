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
            if path is not None:
                if path in excluded_paths:
                    
                    return False
            if path + '/' in excluded_paths or path[:-1] in excluded_paths:
                return False
            return True

        def authorization_header(self, request=None) ->str:
                '''
                '''
                return None
        def current_user(self, request=None) -> TypeVar('User'):
                '''
                '''
                return None