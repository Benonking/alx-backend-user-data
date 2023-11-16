#!/usr/bin/env python3
'''
Module to hash password
'''

import bcrypt
from db import DB
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str):
        '''
        Hash user password using bcrypt
        Args:
            password: passsword string
        Return: return bytes
        '''
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str):
        '''
        register new user to db
        Args:
            email : user email
            password : user password
        Return: new user if doesnt already exist
        Raises: ValueError: If a user already exists with the provided email.
        '''
        existing_user = self._db.find_user_by(email=email)
        if existing_user is None:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)
            return new_user
        else:
            raise ValueError(f'User ${email} already exists')

    def valid_login(self, email, password):
        '''
        Validate user login
        '''
        user = self._db.find_user_by(email=email)
        if user:
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
        return False

    def _generate_uuid(self):
        '''
        genreate unique uudid and return string represantation
        '''
        return str(uuid4())

    def create_session(self, email):
        '''
        create user session
        '''
        user = self._db.find_user_by(email=email)
        if user:
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

    def get_user_from_session_id(self, session_id):

        user = self._db.find_user_by(session_id=session_id)
        if session_id is None or user is None:
            return None
        return user

    def destroy_sesssion(self, user_id):
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

    def get_reset_password_token(self, email: str) -> str:
        '''

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
        password = self._hash_password(password)
        self._db.update_user(
            user.id, hashed_password=password, reset_token=None)
