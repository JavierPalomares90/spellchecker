#!/usr/bin/env python3
# Copyright (C) 2020 Javier Palomares

from symspell import symspell,SymspellDictionary,SymspellVerbosity


def run_scenario1(dictionary_path,bigram_path):
    scenario1_file = "resources/data/scenarios/scenario1.txt"
    with open(scenario1_file,'r',encoding='utf-8') as test_file_text:
        line = test_file_text.readline()
        while line:
            tokens = line.split(' ')




    pass

def main():
    dictionary_path = "resources/data/freq_dict.txt"
    bigram_path = "resources/data/bigram_dict.txt"
    corpus_size = 19684
    dictionary = symspell.load_dictionary(dictionary_path)
    bigram_dictionary = symspell.load_bi_gram_dictionary(bigram_path,corpus_size,dictionary=dictionary)
    run_scenario1(dictionary,bigram_dictionary)

if __name__ == '__main__':
    main()