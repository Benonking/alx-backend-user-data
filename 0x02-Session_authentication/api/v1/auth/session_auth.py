#!/usr/bin/env python3
'''
Session Authentication
'''
from uuid import uuid4

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    '''
    define session authentication
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
        create a session id for user
        '''
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        Return user id based on session_id
        '''
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''
        return authentiicated user based on cokie value
        '''
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        return User.get(user_id)

    def destroy_session(self, request=None):
        '''
        delete user session
        '''
        session_cookie = Auth.session_cookie(request)
        if session_cookie is None or request is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
