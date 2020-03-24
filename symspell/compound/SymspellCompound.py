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

    def lookup_compound(self,input_term):
        return self.lookup_compound(input_term,self.max_dictionary_edit_distance)

    def lookup_compound(self,input_term, max_edit_distance):
        suggestions = list()
        suggestion_parts = list()

        algorithm = DistanceAlgorithms.DistanceAlgorithms.LEVENSHTEIN
        edit_distance = DistanceAlgorithm.DistanceAlgorithm(algorithm)
        terms = Utils.parse_words(input_term)

        # get the best suggestion for each term, else leave it as is.
        terms_combined = False
        num_terms = len(terms)

        for i in range(num_terms):
            suggestions = self.symspell_dictionary.lookup(terms[i],SymspellVerbosity.TOP,max_edit_distance)

            # check for combination
            if i > 0 and terms_combined is False:
                suggestions_for_combination = self.symspell_dictionary.lookup(terms[i-1] + terms[i],SymspellVerbosity.TOP,max_edit_distance)

                if len(suggestions_for_combination) > 0:
                    best1 = suggestion_parts[-1]
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
                    if ((distance1 > 0 ) and \
                        ((suggestions_for_combination[0].distance + 1 < distance1) 
                        or ((suggestions_for_combination[0].distance + 1 == distance1) and
                         (suggestions_for_combination[0].count > best1.count / self.N * best2.count)))):
                        suggestions_for_combination[0].distance =  (suggestions_for_combination[0].distance) + 1
                        suggestion_parts[-1] = suggestions_for_combination[0]
                        terms_combined = True
                        continue
            terms_combined = False

            # always split terms without suggestion. Don't split terms with suggestions. Don't split single char terms
            if (suggestions and (suggestions[0].distance == 0 or len(terms[i]) == 1 )):
                # choose the best suggestion
                suggestion_parts.append(suggestions[0])
            else:
                # no perfect suggestion, split the word into parts
                suggestion_split_best = None

                if suggestions:
                    suggestion_split_best = suggestions[0]
                
                first_term_len = len(terms[i]) 
                if first_term_len > 1:

                    for j in range(1,first_term_len):
                        part1 = terms[i][:j]
                        part2 = terms[i][j:]
                        suggestions1 = self.symspell_dictionary.lookup(part1,SymspellVerbosity.TOP,max_edit_distance)
                        suggestion_split = SymspellSuggestion()

                        if len(suggestions1) > 0:
                            suggestions2 = self.symspell_dictionary.lookup(part2,SymspellVerbosity.TOP,max_edit_distance)
                            
                            if len(suggestions2) > 0:
                                suggestion_split = SymspellSuggestion()
                                # select best suggestion for split pair
                                suggestion_split.term = suggestions1[0].term + " " + suggestions2[0].term

                                suggestions_split_distance = edit_distance.edit_distance(terms[i],suggestion_split.term)
                                if suggestions_split_distance < 0:
                                    suggestions_split_distance = max_edit_distance + 1
                                
                                if suggestion_split_best is not None:
                                    if suggestions_split_distance > suggestion_split_best.distance:
                                        continue
                                    if suggestions_split_distance < suggestion_split_best.distance:
                                        suggestion_split_best = None

                                suggestion_split.distance = suggestions_split_distance 
                                # if bigram exists in bigram dictionary
                                bigram_count = self.bi_grams.get(suggestion_split.term)
                                if bigram_count is not None:
                                    suggestion_split.count = bigram_count

                                    # increase count if split corrections are part of or idential to input

                                    # single term correction exists
                                    if len(suggestions) > 0:
                                        
                                        # remove the single term from suggestions_split
                                        if (suggestions1[0].term + suggestions2[0].term == terms[i]):
                                            suggestion_split.count = max(suggestion_split.count,suggestions[0].count + 2)
                                        elif ((suggestions1[0].term == suggestions[0].term ) or suggestions2[0].term == suggestions[0].term):
                                            # make count bigger than the count of a single term correction
                                            suggestion_split.count = max(suggestion_split.count,suggestions[0].count + 1)
                                    elif (suggestions1[0].term + suggestions2[0].term == terms[i]):
                                        # no single term correction exists
                                        suggestions_split.count = max(suggestion_split.count, max(suggestions1[0].count,suggestions2[0].count) + 2)
                                else:
                                    # The Bayes's prob of the word combination is the product of the 2 word probs
                                    # P(A B) = P(A) * P(B)
                                    # use it to estimate the frequency count of the combination which is then used to rank the best splitting variatn
                                    suggestion_split.count = min(self.min_bi_gram_count,( suggestions1[0].count / self.N * suggestions2[0].count) )
                                if (suggestion_split_best is None or suggestion_split.count > suggestion_split_best.count ):
                                    suggestion_split_best = suggestion_split
                    if suggestion_split_best is not None:
                        suggestion_parts.append(suggestion_split_best)
                    else:
                        si = SymspellSuggestion()
                        si.term = terms[i]
                        # estimate the word probability
                        si.count = 10 / (10 ** len(si.term))
                        si.distance = max_edit_distance + 1
                        suggestion_parts.append(si)
        suggestion = SymspellSuggestion()
        count = self.N
        s = ''
        for si in suggestion_parts:
            s = s + si.term + " "
            count = count * (si.count / self.N)

        # remove trailing whitespace
        s.rstrip()
        suggestion.count = count
        suggestion.term = s
        suggestion.distance = edit_distance.edit_distance(input_term,suggestion.term)

        suggestions_line = list()
        suggestions_line.append(suggestion)

        return suggestions_line



