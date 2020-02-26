#!/usr/bin/env python3
# Copyright (C) 2020 Javier Palomares

import argparse
import os.path
from os import path
import sys
import logging
from .SymspellDictionary import SymspellDictionary
from symspell.compound import SymspellCompound
from utils import Utils

def get_args():
    parser = argparse.ArgumentParser(description="Symspell spelling correction arguments")
    parser.add_argument("-e","--max_edit_distance_precal",required=True, help="The max edit distance per dictionary precalculation")
    parser.add_argument("-d","--dictionary_path",required=True,help="Path to the dictionary")
    args = parser.parse_args()
    return args



def _load_dictionary(dictionary,dictionary_text,term_index,count_index,separator):
    if dictionary is None:
        dictionary = SymspellDictionary()
    line = dictionary_text.readline()
    while line:
        tokens= line.rstrip().split(separator)
        if len(tokens) > count_index:
            term = tokens[term_index]
            count = Utils.parse_int(tokens[count_index])
            if count:
                dictionary.create_dictionary_entry(term,count)
        line = dictionary_text.readline()
    return dictionary
    
def _load_bi_gram_dictionary(dictionary,dictionary_text,terms_index,count_index,separator):
    if dictionary is None:
        dictionary = SymspellDictionary()
    compound_dictionary = SymspellCompound(dictionary)
    line = dictionary_text.readline()
    while line:
        tokens= line.rstrip().split(separator)
        if len(tokens) > count_index:
            # 2 terms
            key = None
            if len(tokens) > 2:
                term1 = tokens[terms_index]
                term2 = tokens[terms_index + 1]
                key = "{term1} {term2}".format(term1=term1,term2=term2)
            else:
                key = tokens[terms_index]
            count = Utils.parse_int(tokens[count_index])
            if count:
                compound_dictionary.create_bi_gram_entry(key,count)

        line = dictionary_text.readline()
    return compound_dictionary

def create_dictionary():
    #TODO: Complete impl
    pass


# load dictionary of the format "<term> <count>"
def load_dictionary(dictionary_path,term_index = 0, count_index = 1,separator=' ',dictionary=None):
    if path.exists(dictionary_path) == False:
        logging.error("Dictionary path {} does not exist".format(dictionary_path))
        sys.exit(-1)
    with open(dictionary_path, 'r', encoding="utf-8") as dictionary_text:
        dictionary = _load_dictionary(dictionary,dictionary_text,term_index,count_index,separator)
    return dictionary

# load bi-gram dictionary of the format "<term1> <term2> <count>"
def load_bi_gram_dictionary(dictionary_path,terms_index = 0,count_index = 2,separator=' ',dictionary=None):
    if path.exists(dictionary_path) == False:
        logging.error("Dictionary path {} does not exist".format(dictionary_path))
        sys.exit(-1)
    with open(dictionary_path, 'r', encoding="utf-8") as dictionary_text:
        dictionary = _load_bi_gram_dictionary(dictionary,dictionary_text,terms_index,count_index,separator)
    return dictionary

def main():
    args = get_args()
    max_edit_distance = args.max_edit_distance_precal
    dictionary_path = args.dictionary_path
    dictionary = load_dictionary(dictionary_path)
    while True:
        query = input("What are you looking for?\n")
        suggestions = dictionary.lookup(query)

    #TODO:  Complete impl
    pass


if __name__ == '__main__':
    main()
