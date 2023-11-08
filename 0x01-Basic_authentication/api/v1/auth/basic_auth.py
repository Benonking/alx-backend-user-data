#!/usr/bin/env python3
'''
class BasicAuth
'''
import base64
import re
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    '''
    Implement request Basic Authentication
    '''

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        '''
                return Base64 part of the Authorix=zation
                header for Basic Authentication
        '''
        if authorization_header is None or \
                not isinstance(authorization_header, str):
            return None
        if authorization_header.startswith('Basic '):
            # return value after basic
            return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        '''
        return decoded value of Base64string
        '''
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None

        try:
            # attempt to decode the base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Decode the bytes to a UTF-8 string and return it
            return decoded_bytes.decode('utf-8',)

        except Exception as e:
            # Handle potential decoding errors
            return None

    def extract_user_credentials(
            self,
            decoded_based64_authorization_header: str) -> Tuple[str, str]:
        '''
        return email and apssword from a base64 decoded string
        '''
        if type(decoded_based64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(
                pattern,
                decoded_based64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeError('User'):
        '''
        Return user instance based on Imail and password
        '''
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        get user object from request
        '''
        # user the authorization method to get the authorization header
        authorization_header = self.authorization_header(request)
        # extract base4 part from hader
        base64_header = self.extract_base64_authorization_header(
                authorization_header)
        token = self.decode_base64_authorization_header(base64_header)
        # extract user credentilas from base64_header
        email, password = self.extract_user_credentials(token)
        # get user instance from credentials
        user = self.user_object_from_credentials(email, password)
        return user
