# Copyright Javier Palomares 2020fro
from symspell.SymspellDictionary import SymspellDictionary
from symspell.SymspellVerbosity import SymspellVerbosity
import re

class SymspellCompound(SymspellDictionary):
    def __init__(self, count_threshold=1, max_dictionary_edit_distance=2, prefix_len=7):
        super().__init__(count_threshold=count_threshold, max_dictionary_edit_distance=max_dictionary_edit_distance, prefix_len=prefix_len)

    def lookup_compound(input):
        return lookup_compound(input,self.max_dictionary_edit_distance)

    @staticmethod
    def parse_words(text):
        return re.findall('[A-Za-z\']+(?:\`[A-Za-z]+)?',text.lower())
    
    def lookup_compound(input, max_edit_distance):
        terms = parse_words(input)
        suggestions = []
        suggestion_parts = []

        edit_distance = EditDistance()

        # get the best suggestion for each term, else leave it as is.
        terms_combined = False

        for i in range(len(terms)):
            suggestions = super().lookup(terms[i],SymspellVerbosity.TOP,max_edit_distance)

            # check for combination
            if i > 0 and terms_combined is False:
                suggestions_for_combination = super.lookup(terms[i-1] + terms[i],SymspellVerbosity.TOP,max_edit_distance)

                if len(suggestions_for_combination) > 0:
                    best1 = suggestion_parts[len(suggestions_for_combination) - 1]
                    #TODO: Complete impl
                    best2 = None

                





