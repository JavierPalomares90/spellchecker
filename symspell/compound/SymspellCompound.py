# Copyright Javier Palomares 2020fro
from symspell.SymspellDictionary import SymspellDictionary
import re

class SymspellCompound(SymspellDictionary):
    def __init__(self, count_threshold=1, max_dictionary_edit_distance=2, prefix_len=7):
        super().__init__(count_threshold=count_threshold, max_dictionary_edit_distance=max_dictionary_edit_distance, prefix_len=prefix_len)

    def lookup_compound(input):
        return lookup_compound(input,self.max_dictionary_edit_distance)

    @staticmethod
    def parse_words(text):
        matches = re.match("['’\w-[_]]+",text.lower())
        #TODO: Complete impl
        return matches
    
    def lookup_compound(input, max_edit_distance):
        terms = parse_words(input)


