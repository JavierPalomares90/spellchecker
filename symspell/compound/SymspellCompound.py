# Copyright Javier Palomares 2020fro
from symspell.SymspellDictionary import SymspellDictionary
from symspell.SymspellVerbosity import SymspellVerbosity
from symspell.SymspellSuggestion import SymspellSuggestion
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
                    best2 = SymspellSuggestion()
                    if len(suggestions) > 0:
                        best2 = suggestions[0]
                    else:
                        # unknown word
                        best2.term = terms[i]
                        # estimated edit distance
                        best2.distance = max_edit_distance + 1
                        # estimated word occurance prob
                        best2.count = 10.0 / (10.0 ** len(best2.term))
                    # distance1 = distance between 2 split terms and their best corrections
                    distance1 = best1.distance + best2.distance
                    #TODO: waht the hell is N?
                    if ((distance1 > 0 ) and ((suggestions_for_combination[0].distance + 1 < distance1) or ((suggestions_for_combination[0].distance + 1 == distance1) and (suggestions_for_combination[0].count > best1.count / SymSpell.N * best2.count))
                        suggestions_for_combination[0].distance += 1
                        suggestions_for_combination[len(suggestions_for_combination) -1 ] = suggestions_for_combination[0]
                        terms_combined = True
                        # GOTO: nextTerm
            terms_combined = False

            # always split terms without suggestion. Don't split terms with suggestions. Don't split single char terms
            if (len(suggestions) > 0 and (suggestions[0].distance == 0 or len(terms[i]) == 1 )):
                # choose the best suggestion
                suggestion_parts.append(suggestions[0])
            else:
                # no perfect suggestion, split the word into parts
                suggestion_split_best = None

                if len(suggestions) > 0:
                    suggestion_split_best = suggestions[0]
                
                if len(terms[i]) > 1:

                    for j in range(len(terms)):
                        part1 = terms[i][0:j]
                        part2 = terms[i][j:]
                        suggestions_split = SymspellSuggestion()
                        suggestions1 = super().lookup(part1,SymspellVerbosity.TOP,max_edit_distance)

                        if len(suggestions1) > 0:
                            suggestions2 = super().lookup(part2,SymspellVerbosity.TOP,max_edit_distance)
                            
                            if len(suggestions2) > 0:
                                # select best suggestion for split pair
                                # TODO: Complete impl
                                pass







                





