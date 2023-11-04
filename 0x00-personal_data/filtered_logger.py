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
        separator: str) -> str:
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
    return re.sub(
            f'({pattern})=[^{separator}]*', f'\\1={redaction}', message
            )


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
    user_data_logger = logging.getLogger("user_data")
    user_data_logger.setLevel(logging.INFO)
    user_data_logger.propagate = False

    handler = logging.StreamHandler()

    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_data_logger.addHandler(handler)
    return user_data_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
    connect to decure db
    '''
    db_config = {
        "user": os.getenv("PERSONAL_DATA_DB_USERNAME") or "root",
        "password": os.getenv("PERSONAL_DATA_DB_PASSWORD") or "",
        "host": os.getenv("PERSONAL_DATA_DB_HOST") or "localhost",
        "database": os.getenv("PERSONAL_DATA_DB_NAME")
        }
    conn = mysql.connector.connect(**db_config)
    return conn


def main():
    """
    main entry point
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
