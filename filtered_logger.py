#!/usr/bin/env python3
'''
Module filter_loggger
'''
import re
from typing import List


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
