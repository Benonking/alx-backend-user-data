#!/usr/bin/env python3
'''
Module to hash password
'''

import bcrypt
from db import DB
from uuid import uuid4
from typing import Optional, Union
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''
    Hash user password using bcrypt
    Args:
        password: passsword string
    Return: return bytes
    '''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    '''
    genreate unique uudid and return string represantation
    '''
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        register new user to db
        Args:
            email : user email
            password : user password
        Return: new user if doesnt already exist
        Raises: ValueError: If a user already exists with the provided email.
        '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        '''
        Validate user login
        '''
        
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False
        return False
    

    def create_session(self, email: str) -> Union[str, None]:
        '''
        create user session
        '''
        user = self._db.find_user_by(email=email)
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        '''
        get user from session_id
        Args:
            session_id: session id of user
        Returns: user with specified session_id or None
        '''
        user = self._db.find_user_by(session_id=session_id)
        if session_id is None or user is None:
            return None
        return user

    def destroy_sesssion(self, user_id) -> None:
        '''
         Destroy the session for the user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            None
        '''
        user = self._db.find_user_by(id=user_id)
        self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> Union[str, None]:
        '''
        Reset user password_token
        Args:
            email - user email
        Returns: new token
        Raises: ValueError is user isnt found
        '''
        user = self._db.find_user_by(email=email)
        if user is None:
            raise ValueError
        new_token = str(uuid4())
        self._db.update_user(user.id, reset_token=new_token)
        return new_token

    def update_password(self, reset_token: str, password: str) -> None:
        '''
        update Users password using reset token
        Args:
            reset_token: password reset token
            password: password to be reset
        Return: None
        Raises: ValueError if reset token not given
        '''
        user = self._db.find_user_by(reset_token=reset_token)
        if reset_token is None:
            raise ValueError
        password = _hash_password(password)
        self._db.update_user(
            user.id, hashed_password=password, reset_token=None)
