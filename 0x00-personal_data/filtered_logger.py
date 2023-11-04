#!/usr/bin/env python3
'''
Module filter_loggger
'''
import re
from typing import List
import logging


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
