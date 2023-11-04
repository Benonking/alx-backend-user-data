#!/usr/bin/env python3
'''
Hash password
'''
import bcrypt




def hash_password(password: str) -> str:
    '''
    hash user password
    '''
    salt = bcrypt.gensalt()
    hashed_paswd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_paswd

