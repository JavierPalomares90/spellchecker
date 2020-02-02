#!/usr/bin/env python3
# Copyright Javier Palomares 2020

import re
import argparse
import os.path
from os import path
import sys
from collections import Counter

LETTERS = 'abcdefghijklmnopqrstuvwxyz'

def get_args():
    parser = argparse.ArgumentParser(description="Scrape text from a wikipedia article")
    parser.add_argument("-d","--dictionary",required=True, help="The text file to use for the dictionary")
    args = parser.parse_args()
    return args

def get_dictionary_terms(dictionary_path):
    if path.exists(dictionary_path) == False:
        print("Dictionary path {} does not exist".format(dictionary_path))
        sys.exit(-1)

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

def get_valid_terms(words,valid_terms):
    return set(w for w in words if w in valid_terms)

def _words_with_edit_distance_1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in LETTERS]
    inserts    = [L + c + R               for L, R in splits for c in LETTERS]
    return set(deletes + transposes + replaces + inserts)

def get_words_within_edit_distance(word,edit_distance):
    if edit_distance == 0:
        return word
    if edit_distance == 1:
        return _words_with_edit_distance_1(word)
    else:
        s = set()
        for e1 in get_words_within_edit_distance(word,edit_distance-1):
            for e2 in _words_with_edit_distance_1(e1):
                s.add(e2)
        return s

def get_candidate_words(word,valid_terms):
    valid_terms_in_word = get_valid_terms([word],valid_terms)
    if len(valid_terms_in_word) != 0:
        return valid_terms_in_word
    edit_1_terms = get_words_within_edit_distance(word,1)
    valid_terms_in_edit_1 = get_valid_terms(edit_1_terms,valid_terms)
    if len(valid_terms_in_edit_1) != 0:
        return edit_1_terms
    edit_2_terms = get_words_within_edit_distance(word,2)
    valid_terms_in_edit_2 = get_valid_terms(edit_2_terms,valid_terms)
    if len(valid_terms_in_edit_2) != 0:
        return edit_2_terms
    return None

def get_error_model(dictionary):
    dictionary_terms = get_dictionary_terms(dictionary)
    term_frequencies = get_term_frequencies(dictionary_terms)
    term_probabilities = get_term_probabilities(term_frequencies)
    return dictionary_terms,term_probabilities

def get_spelling_correction(word,error_model):
    candidate_words = get_candidate_words(word,error_model.keys())
    return max(candidate_words,key=error_model)

def main():
    args = get_args()
    dictionary = args.dictionary
    dictionary_terms,error_model = get_error_model(dictionary)
    # get the word from the user to check for spelling
    while True:
        word = input("Try my spelling:\n")
        correction = get_spelling_correction(word,error_model)
        print("I suggest you spell that as {}".format(correction))

if __name__ == '__main__':
    main()
