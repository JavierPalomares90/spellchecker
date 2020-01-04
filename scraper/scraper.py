#!/usr/bin/env python3
# Copyright Javier Palomares 2020

##
## Python tool written to scrape text from wikipedia
#

import argparse
import heapq
import re
from urllib.request import urlopen,urlretrieve
from urllib.parse import urlparse, urlsplit
import os
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import errno
import requests

def get_args():
    parser = argparse.ArgumentParser(description="Scrape text from a wikipedia article")
    parser.add_argument("-u","--url",required=True, help="The url to scrape text from")
    parser.add_argument("-f","--filepath",required=True,help="Where to save the text to")
    args = parser.parse_args()
    return args

def scrape_url(url,filepath):
    pass

def main():
    args = get_args()
    url = args.url
    filepath = args.filepath
    scrape_url(url,filepath)

if __name__ == '__main__':
    main()