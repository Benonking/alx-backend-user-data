#!/usr/bin/env python3
'''
Hash password
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''
    hash user password
    '''

    salt = bcrypt.gensalt()
    hashed_paswd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_paswd


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
    check if password is correct
    '''
    return bcrypt.checkpw(password.encode(), hashed_password)
