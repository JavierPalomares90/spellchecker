#!/usr/bin/env python3
# Copyright (C) 2020 Javier Palomares
from norvig import norvig
from symspell import symspell,SymspellDictionary,SymspellVerbosity
import logging


def run_norvig():
    logging.debug("runing norvig")
    print("You picked norvig")
    print("Needed arguments: \n 1. path to dictionary file 2. Max edit distance (default is 2)\n")
    dictionary_path = input("Pass in the path to the dictionary file\n")
    max_edit_distance = input("What is the max edit distance. Hit enter for default of 2\n")
    try:
        max_edit_distance = int(max_edit_distance)
    except ValueError:
        max_edit_distance = 2
    logging.debug("getting dictionary from : {}".format(dictionary_path))
    dictionary_terms,error_model = norvig.get_error_model(dictionary_path)
    while True:
        word = input("Try my spelling. One word at a time:\n")
        correction = norvig.get_spelling_correction(word,dictionary_terms,error_model,max_edit_distance)
        if correction is None:
            print("I don't have a suggestion for you.\n")
        else:
            print("I suggest you spell that as:\n{}".format(correction))

def run_symspell():
    logging.debug("runing symspell")
    print("You picked norvig")
    print("Needed arguments: \n 1. path to dictionary frequency map (corpus) 2. max edit distance(default 3. corpus size\n")
    dictionary_path = input("Pass in the path to the dictionary frequency map\n")
    max_edit_distance = input("What is the max edit distance. Hit enter for default of 2\n")
    try:
        max_edit_distance = int(max_edit_distance)
    except ValueError:
        max_edit_distance = 2
    corpus_size = input("What is the corpus size\n")
    corpus_size = int(corpus_size)

    dictionary = symspell.load_dictionary(dictionary_path)
    while True:
        word = input("Try my spelling. One word at a time:\n")
        correction = dictionary.lookup(word,verbosity=SymspellVerbosity.SymspellVerbosity.TOP,max_edit_distance=max_edit_distance,include_unknown=False)
        if correction is None:
            print("I don't have a suggestion for you.\n")
        else:
            print("I suggest you spell that as:\n{}".format(correction))



def run_symspell_compound():
    logging.debug("runing symspell compound")
    print("Needed arguments: \n 1. path to dictionary frequency map 2. path to bi gram frequency map 3. max edit distance (default is 2)4. corpus size\n")
    dictionary_path = input("Pass in the path to the dictionary frequency map\n")
    bigram_dictionary_path = input("Pass in the path to the bi gram frequency map\n")
    max_edit_distance = input("What is the max edit distance. Hit enter for default of 2\n")
    try:
        max_edit_distance = int(max_edit_distance)
    except ValueError:
        max_edit_distance = 2
    corpus_size = input("What is the corpus size\n")
    corpus_size = int(corpus_size)
    dictionary = symspell.load_dictionary(dictionary_path)
    bigram_dictionary = symspell.load_bi_gram_dictionary(bigram_dictionary_path,corpus_size,dictionary=dictionary)
    while True:
        input_terms = input("Try my spelling. You may enter multiple words at once")
        suggestions = bigram_dictionary.lookup_compound(input_terms, max_edit_distance=max_edit_distance)
        # display suggestion term, edit distance, and term frequency
        if suggestions:
            print("I suggest:")
            for suggestion in suggestions:
                print(suggestion)
        else:
            print("I don't have a suggestion for you.\n")


def main():
    print("Welcome to spellchecker. Algorithm options:")
    print("1 - Norvig")
    print("2 - Symspell")
    print("3 - Symspell Compound (using bigram)")
    print("4 - Symspell using fuzzy")
    response = None

    while response not in {"1","2","3","4"}:
        response = input("Select the algorithm to use:\n")
        if(response == "1"):
            run_norvig()
        if(response == "2"):
            run_symspell()
        if response in {"3","4"}:
            run_symspell_compound()


if __name__ == '__main__':
    main()
