#!/usr/bin/env python3
# Copyright Javier Palomares 2020

import re
import argparse
from collections import Counter


def get_args():
    parser = argparse.ArgumentParser(description="Scrape text from a wikipedia article")
    parser.add_argument("-d","--dictionary",required=True, help="The text file to use for the dictionary")
    args = parser.parse_args()
    return args

def get_dictionary_terms(dictionary_path):
    # get all the words in the dictionary.
    with open(dictionary_path,'r',encoding="utf-8") as dictionary_text:
    # dictionary is text sensitive
        terms = re.findall(r'\w+',dictionary_text.read())
    return terms

def get_term_frequencies(dictionary_terms):
    frequencies = Counter(dictionary_terms)
    return frequencies

def get_term_probabilities(term_freqs):
    num_words = sum(term_freqs.values())
    term_probs = term_freqs.copy()
    for term in term_probs:
        term_probs[term] = term_probs[term] / num_words
    return term_probs

def get_candidate_words(word,valid_terms):
    #TODO: Complete impl


def get_error_model(dictionary):
    dictionary_terms = get_dictionary_terms(dictionary)
    term_frequencies = get_term_frequencies(dictionary_terms)
    term_probabilities = get_term_probabilities(term_frequencies)
    return term_probabilities

def get_spelling_correction(word,error_model):
    candidate_words = get_candidate_words(word,error_model.keys())


def main():
    args = get_args()
    dictionary = args.dictionary
    dictionary_terms,error_model = get_error_model(dictionary)
    # get the word from the user to check for spelling
    while True:
        word = input("Try my spelling:\n")
        correction = get_spelling_correction(word,error_model)

    




if __name__ == '__main__':
    main()
