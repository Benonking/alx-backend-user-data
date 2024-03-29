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
    return bcrypt.hashpw(password.encode('utf-8'), salt)


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
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        '''
        get user from session_id
        Args:
            session_id: session id of user
        Returns: user with specified session_id or None
        '''
        try:
            user = self._db.find_user_by(session_id=session_id)
            if session_id is None or user is None:
                return None
        except NoResultFound:
            return None

        return user

    def destroy_sesssion(self, user_id: int) -> None:
        '''
         Destroy the session for the user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            None
        '''
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

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
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError
        new_token = _generate_uuid()
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
        if reset_token is None or password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        password = _hash_password(password)
        self._db.update_user(
            user.id, hashed_password=password, reset_token=None)
