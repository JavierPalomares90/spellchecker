#!/usr/bin/env python3
# Copyright Javier Palomares 2020

import argparse
import os.path
from os import path
import sys
from .symspell_dictionary import symspell_dictionary

def get_args():
    parser = argparse.ArgumentParser(description="Symspell spelling correction arguments")
    parser.add_argument("-i","--initial_capacity",required=True, help="The initial capacity of the dictionary")
    parser.add_argument("-e","--max_edit_distance_precal",required=True, help="The max edit distance per dictionary precalculation")
    parser.add_argument("-d","--dictionary_path",required=True,help="Path to the dictionary")
    args = parser.parse_args()
    return args



def _load_dictionary(dictionary_text,term_index, count_index,separator):
    dictionary = symspell_dictionary()
    line = dictionary_text.getline()
    while line:
        tokens = line.split(separator)
        term = tokens[term_index]
        count = int(tokens[count_index])
        symspell_dictionary.create_dictionary_entry(term,count)
        line = dictionary_text.getline()
    return dictionary


def load_dictionary(dictionary_path,term_index = 0, count_index = 1,separator=','):
    if path.exists(dictionary_path) == False:
        print("Dictionary path {} does not exist".format(dictionary_path))
        sys.exit(-1)
    with open(dictionary_path, 'r', encoding="utf-8") as dictionary_text:
        dictionary = _load_dictionary(dictionary_text,term_index,count_index,separator)
    return dictionary


def main():
    args = get_args()
    initial_capacity = args.initial_capacity
    max_edit_distance = args.max_edit_distance_precal
    dictionary_path = args.dictionary_path
    dictionary = load_dictionary(dictionary_path)

    #TODO:  Complete impl
    pass


if __name__ == '__main__':
    main()
