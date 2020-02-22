# Copyright (C) 2020 Javier Palomares

import logging

def parse_int(s):
    value = None
    try:
        value = int(s)
    except expression as identifier:
        logging.error("Unable to parse {} to int".format(s))
    return value
