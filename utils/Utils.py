# Copyright (C) 2020 Javier Palomares

import logging
import hashlib
import sys
import re

def parse_int(s):
    value = None
    try:
        value = int(s)
    except ValueError:
        logging.error("Unable to parse {} to int".format(s))
    return value

def parse_words(text):
    return re.findall('[A-Za-z\']+(?:\`[A-Za-z]+)?',text.lower())

def get_string_hash(s):
    hash = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10 ** 8
    return hash

def sort_suggestions(suggestions):
    suggestions.sort()
