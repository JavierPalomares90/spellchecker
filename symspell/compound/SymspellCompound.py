# Copyright (C) Javier Palomares 2020

from symspell.SymspellDictionary import SymspellDictionary
from symspell.SymspellVerbosity import SymspellVerbosity
from symspell.SymspellSuggestion import SymspellSuggestion
from edit import DistanceAlgorithms
from edit import DistanceAlgorithm
from utils import Utils
import re
import sys

class SymspellCompound(SymspellDictionary):
    def __init__(self, symspell_dictionary,corpus_size, count_threshold=1, max_dictionary_edit_distance=2, prefix_len=7):
        self.bi_grams = dict()
        self.symspell_dictionary = symspell_dictionary
        self.min_bi_gram_count = sys.maxsize
        self.N = corpus_size

    def create_bi_gram_entry(self,key,count):
        if count < 0:
            if self.count_threshold > 0:
                return False
        self.bi_grams[key] = count
        if count < self.min_bi_gram_count:
            self.min_bi_gram_count = count
        return True

    def lookup_compound(self,input):
        return lookup_compound(input,self.max_dictionary_edit_distance)

    def lookup_compound(self,input, max_edit_distance):
        suggestions = list()
        suggestion_parts = list()

        algorithm = DistanceAlgorithms.DistanceAlgorithms.LEVENSHTEIN
        edit_distance = DistanceAlgorithm.DistanceAlgorithm(algorithm)
        terms = Utils.parse_words(input)

        # get the best suggestion for each term, else leave it as is.
        terms_combined = False
        num_terms = len(terms)

        for i in range(num_terms):
            suggestions = self.symspell_dictionary.lookup(terms[i],SymspellVerbosity.TOP,max_edit_distance)

            # check for combination
            if i > 0 and terms_combined is False:
                suggestions_for_combination = self.symspell_dictionary.lookup(terms[i-1] + terms[i],SymspellVerbosity.TOP,max_edit_distance)

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
                    if ((distance1 > 0 ) and \
                        ((suggestions_for_combination[0].distance + 1 < distance1) 
                        or ((suggestions_for_combination[0].distance + 1 == distance1) and
                         (suggestions_for_combination[0].count > best1.count / self.N * best2.count)))):
                        suggestions_for_combination[0].distance =  (suggestions_for_combination[0].distance) + 1
                        suggestions_for_combination[len(suggestions_for_combination) - 1 ] = suggestions_for_combination[0]
                        terms_combined = True
                        # GOTO: nextTerm
            terms_combined = False

            # always split terms without suggestion. Don't split terms with suggestions. Don't split single char terms
            if (suggestions and (suggestions[0].distance == 0 or len(terms[i]) == 1 )):
                # choose the best suggestion
                suggestion_parts.append(suggestions[0])
            else:
                # no perfect suggestion, split the word into parts
                suggestion_split_best = None

                if len(suggestions) > 0:
                    suggestion_split_best = suggestions[0]
                
                first_term_len = len(terms[i]) 
                if first_term_len > 1:

                    for j in range(1,first_term_len):
                        part1 = terms[i][:j]
                        part2 = terms[i][j:]
                        suggestions_split = SymspellSuggestion()
                        suggestions1 = super().lookup(part1,SymspellVerbosity.TOP,max_edit_distance)

                        if len(suggestions1) > 0:
                            suggestions2 = super().lookup(part2,SymspellVerbosity.TOP,max_edit_distance)
                            
                            if len(suggestions2) > 0:
                                # select best suggestion for split pair
                                suggestion_split.term = suggestions1[0].term + " " + suggestions2[0].term

                                distance2 = edit_distance.compare(terms[i],suggestion_split.term,max_edit_distance)
                                if distance2 < 0:
                                    distance2 = max_edit_distance + 1
                                
                                if suggestion_split_best is not None:
                                    if distance2 > suggestion_split_best.distance:
                                        continue
                                    if distance2 < suggestion_split_best.distance:
                                        suggestion_split_best = None

                                suggestion_split.distance = distance2
                                # if bigram exists in bigram dictionary
                                bigram_count = self.bigrams[suggestion_split.term] 
                                if bigram_count is not None:
                                    suggestion_split.count = bigram_count

                                    # increaase count if split corrections are part of or idential to input

                                    # single term correction exists
                                    if len(suggestions) > 0:
                                        
                                        # remove the single term from suggestions_split
                                        if (suggestions1[0].term + suggestions2[0].term == terms[i]):
                                            # TODO: Check why +2 here
                                            suggestion_split.count = max(suggestion_split.count,len(suggestions[0]) + 2)
                                        elif ((suggestions1[0].term == suggestions[0].term ) or suggestion2[0].term == suggestions[0].term):
                                            # make count bigger than the count of a single term correction
                                            suggestion_split.count = max(suggestion_split.count,suggestions[0].count + 1)
                                    elif (suggestions1[0].term + suggestions2[0].term == terms[i]):
                                        # no single term correction exists
                                        suggestions_split.count = max(suggestion_split.count, max(suggestions1[0].count,suggestion2[0].count) + 2)
                                else:
                                    # The Bayes's prob of the word combination is the product of the 2 word probs
                                    # P(A B) = P(A) * P(B)
                                    # use it to estimate the frequency count of the combination which is then used to rank the best splitting variatn
                                    suggestion_split.count = min(self.bigram_count_min,( suggestions1[0].count / Symspell.N * suggestions2[0].count) )
                                if (suggestion_split_best is None or suggestion_split.count > suggestion_split_best.count ):
                                    suggestion_split_best = suggestion_split
                    pass
                    if suggestion_split_best is not None:
                        #TODO: WTF is suggestion_parts
                        suggestion_parts.append(suggestion_split_best)
                    else:
                        si = SymspellSuggestion()
                        si.term = terms[i]
                        # estimate the word probability
                        si.count = 10 / (10 ** len(si.term))
                        si.distance = max_edit_distance + 1
                        #TODO Where is suggestion_parts defined
                        suggestion_parts.append(si)
        suggestion = SymspellSuggestion()
        #TODO: Fix N
        count = Symspell.N
        s = ''
        for si in suggestions_parts:
            s = s + si.term + " "
            count = count * (si.count /Symspell.N)

        suggestion.count = count
        suggestion.term = s
        suggestion.distance = edit_distance.compare(input,suggestion.term,sys.maxsize)

        suggestions_line = list()
        suggestions_line.append(suggestion)

        return suggestions_line




