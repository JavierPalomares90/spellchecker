# Copyright (C) 2020 Javier Palomares
import pkg_resources
from symspell import symspell,SymspellDictionary,SymspellVerbosity

dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")
bigram_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
dictionary = symspell.load_dictionary(dictionary_path)
suggestions = dictionary.lookup("whereis",verbosity=SymspellVerbosity.SymspellVerbosity.TOP,max_edit_distance=2,include_unknown=False)


# lookup suggestions for multi-word input strings (supports compound
# splitting & merging)
bigram_dictionary = symspell.load_bi_gram_dictionary(bigram_path,dictionary=dictionary)
input_term = ("whereis th elove hehad dated forImuch of thepast who "
              "couqdn'tread in sixtgrade and ins pired him")
# max edit distance per lookup (per single word, not per whole input string)
suggestions = dictionary.lookup_compound(input_term, max_edit_distance=2)
# display suggestion term, edit distance, and term frequency
for suggestion in suggestions:
    print(suggestion)


