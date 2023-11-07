#!/usr/bin/env python3
'''
class BasicAuth
'''
import base64
from api.v1.auth.auth import Auth


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
            decoded_based64_authorization_header: str) -> (str, str):
        '''
        return email and apssword from a base64 decoded string
        '''
        if decoded_based64_authorization_header is None or \
                not isinstance(
                    decoded_based64_authorization_header,
                    str) or ":" not in decoded_based64_authorization_header:
            return (None, None)
        result = decoded_based64_authorization_header.split(':')
        return tuple(result)
