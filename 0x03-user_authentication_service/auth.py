#!/usr/bin/env python3
'''
Module to hash password
'''

import bcrypt


def _hash_password(password: str):
    '''
    Hash user password using bcrypt
    Args:
            password: passsword string
    Return: return bytes
    '''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
