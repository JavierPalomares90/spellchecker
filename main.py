#!/usr/bin/env python3
# Copyright (C) 2020 Javier Palomares
from norvig import norvig
from symspell import symspell
import logging


def run_norvig():
    logging.debug("runing norvig")
    print("You picked norvig")
    print("Needed arguments: \n 1. Dictionary file 2. Max edit distance (default is 2)\n")
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
    logging.debug("runing norvig")
    print("You picked norvig")

def main():
    print("Welcome to spellchecker. Algorithm options:")
    print("1 - Norvig")
    print("2 - Symspell with bi grams")
    print("3 - Symspell with fuzzy")
    response = None

    while response not in {"1","2","3"}:
        response = input("Select the algorithm to use:\n")
        if(response == "1"):
            run_norvig()
        if(response == "1"):
            run_symspell()


if __name__ == '__main__':
    main()
