# Copyright (C) 2020 Javier Palomares
import pkg_resources
from symspell import symspell,SymspellDictionary


dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")
bigram_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
dictionary = symspell.load_dictionary(dictionary_path)
symspell.load_bi_gram_dictionary(bigram_path,dictionary=dictionary)




