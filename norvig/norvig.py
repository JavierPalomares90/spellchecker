#!/usr/bin/env python3
# Copyright (C) 2020 Javier Palomares

import re
import argparse
import os.path
from os import path
import sys
from collections import Counter

LETTERS = "abcdefghijklmnopqrstuvwxyz&.,!@#$()-+'"

def get_args():
    parser = argparse.ArgumentParser(description="Scrape text from a wikipedia article")
    parser.add_argument("-d","--dictionary",required=True, help="The text file to use for the dictionary")
    parser.add_argument("-e","--max_edit_distance",required=False, default=2,help="The maximum edit distance to use in the algorithm")
    args = parser.parse_args()
    return args

def get_dictionary_terms(dictionary_path):
    if path.exists(dictionary_path) == False:
        print("Dictionary path {} does not exist".format(dictionary_path))
        sys.exit(-1)

    # get all the words in the dictionary.
    with open(dictionary_path,'r',encoding="utf-8") as dictionary_text:
        # dictionary is case sensitive. We want to keep special characters, so we'll simply split on whitespace
        terms = dictionary_text.read().split()
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
    valid = set()
    for w in words:
        casefold_w = w.casefold()
        if casefold_w in valid_terms:
            spellings = set(valid_terms[casefold_w])
            valid |= spellings
    return valid

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

def get_candidate_words(word,valid_terms,max_edit_distance):
    valid_terms_in_word = get_valid_terms([word],valid_terms)
    if len(valid_terms_in_word) != 0:
        return valid_terms_in_word
    for i in range(max_edit_distance):
        edit_i_terms = get_words_within_edit_distance(word,i+1)
        valid_terms_in_edit_i = get_valid_terms(edit_i_terms,valid_terms)
        if (len(valid_terms_in_edit_i) != 0):
            return valid_terms_in_edit_i
    return None

def get_casefold_dictionary(dictionary_terms):
    terms = dict()
    # iterate over all the dictionary
    for term in dictionary_terms:
        # casefold key
        key = term.casefold()

        # if the key is not in the map, add the term as a new list
        if key not in terms:
            value = [term]
            terms[key] = value
            
        else:
            # add it to the list
            values_list = terms[key]
            values_list.append(term)
            terms[key] = values_list
    return terms


def get_error_model(dictionary):
    # get all the terms in the dictionary
    dictionary_terms = get_dictionary_terms(dictionary)
    # get the frequency and probability of each unique term in the dictionary
    term_frequencies = get_term_frequencies(dictionary_terms)
    term_probabilities = get_term_probabilities(term_frequencies)

    # dictionaries are case senstivite. Get a case insensitive lookup from casefold() keys to cased spellings
    # return this as a dictionary for quick lookups
    terms = get_casefold_dictionary(term_frequencies)

    return terms,term_probabilities

def get_spelling_correction(word,dictionary_terms,error_model,max_edit_distance):
    candidate_words = get_candidate_words(word,dictionary_terms,max_edit_distance)
    if candidate_words is None:
        return None
    return max(candidate_words,key= lambda k: error_model[k])

def main():
    args = get_args()
    dictionary = args.dictionary
    max_edit_distance = args.max_edit_distance
    dictionary_terms,error_model = get_error_model(dictionary)
    # get the word from the user to check for spelling
    while True:
        word = input("Try my spelling. One word at a time:\n")
        #TODO: handle special characters
        correction = get_spelling_correction(word,dictionary_terms,error_model,max_edit_distance)
        if correction is None:
            print("I don't have a suggestion for you.\n")
        else:
            print("I suggest you spell that as:\n{}".format(correction))

if __name__ == '__main__':
    main()
