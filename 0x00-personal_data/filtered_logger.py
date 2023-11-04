#!/usr/bin/env python3
'''
Module filter_loggger
'''
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> None:
    '''
    function to obscate a property
    Args:
        fileds: list of strings that contain property files to obscate
        redaction: string representing by what the filed will be replaced
        message: log line
        separator: a string representing by which character
                    is separating all fields in the log line
    TECNIC USE re.sub
    '''
    pattern = '|'.join(fields)
    return re.sub(f'({pattern})=[^{separator}]*', f'\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''instanciate Redacting class'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' create an instance of Readcting
            class and apply filtered_datum to it
        '''
        # get message from logger
        message = super(RedactingFormatter, self).format(record)
        # filter the message using filter_datum
        filtered = filter_datum(
            self.fields,
            self.REDACTION,
            message,
            self.SEPARATOR
        )

        return filtered


def get_logger() -> logging.Logger:
    '''create a logger'''
    # create a logger named "user_data"
    user_data_logger = logging.getLogger("user_data")
    user_data_logger.setLevel(logging.INFO)
    user_data_logger.propagate = False

    # create StremHandler

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))

    # add the handler to the logger
    user_data_logger.addHandler(handler)

    return user_data_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
    connect to decure db
    '''
    try:
        db_config = {
            "user": os.getenv("PERSONAL_DATA_DB_USERNAME"),
            "password": os.getenv("PERSONAL_DATA_DB_PASSWORD"),
            "host": os.getenv("PERSONAL_DATA_DB_HOST"),
            "database": os.getenv("PERSONAL_DATA_DB_NAME")
        }
        if None in db_config.values():
            raise ValueError("one of the enviroment varibales not set")
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
