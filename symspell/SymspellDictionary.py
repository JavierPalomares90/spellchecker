# Copyright (C) 2020 Javier Palomares

import hashlib
import sys
from .SymspellSuggestion import SymspellSuggestion
from .SymspellVerbosity import SymspellVerbosity
from edit import DistanceAlgorithms
from edit import DistanceAlgorithm
import logging


class SymspellDictionary:

    def __init__(self,count_threshold = 1,max_dictionary_edit_distance=2, prefix_len = 7):
        self.count_threshold= count_threshold
        self.max_dictionary_word_length = 0
        self.min_bi_gram_count = sys.maxsize
        self.max_dictionary_edit_distance = max_dictionary_edit_distance
        self.prefix_length = prefix_len
        '''
            // Dictionary that contains a mapping of lists of suggested correction words to the hashCodes
            // of the original words and the deletes derived from them. Collisions of hashCodes is tolerated,
            // because suggestions are ultimately verified via an edit distance function.
            // A list of suggestions might have a single suggestion, or multiple suggestions.
        '''
        self.deletes = dict()
        '''
            // Dictionary of unique words that are below the count threshold for being considered correct spellings.
        '''
        self.below_threshold_words = dict()
        '''
            // Dictionary of unique correct spelling words, and the frequency count for each word.
        '''
        self.words = dict()
        '''
            // Dictionary of unique bigrams, and the frequency count for each word.
        '''
        self.bi_grams = dict()

    @staticmethod
    def _get_edits(word,edit_distance,words_set,max_dictionary_edit_distance):
        # delete edits only
        edit_distance += 1
        word_len = len(word)
        if word_len > 1:
            for i in range(word_len):
                # remove the ith character from the word
                delete_edit = word[:i] + word[i+1:]
                if (delete_edit in words_set) == False:
                    words_set.add(delete_edit)
                    # recursive find other delete edits
                    if edit_distance < max_dictionary_edit_distance:
                        SymspellDictionary._get_edits(delete_edit,edit_distance,words_set,max_dictionary_edit_distance)
        return words_set

    @staticmethod
    def _get_string_hash(s):
        hash = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10 ** 8
        return hash

    @staticmethod
    def _sort_suggestions(suggestions):
        #TODO: Complete impl
        return suggestions 


    @staticmethod
    def _get_edits_prefix(term,max_dictionary_edit_distance,prefix_length):
        edits = set()
        if len(term) <= max_dictionary_edit_distance:
            # word is too short, add empty string
            edits.add("")
        if len(term) > prefix_length:
            term = term[0:prefix_length]
        edits.add(term)
        return SymspellDictionary._get_edits(term,0,edits,max_dictionary_edit_distance)


    # Check if all the delete chars are present in the suggestion prefix order
    @staticmethod
    def delete_in_suggestion_prefix(delete,delete_len, suggestion,suggestion_len):
        #TODO: Complete impl

        return True


    def create_bi_gram_entry(self,key,count):
        if count < 0:
            if self.count_threshold > 0:
                return False
        self.bi_grams[key] = count
        if count < self.min_bi_gram_count:
            self.min_bi_gram_count = count
        return True

    '''
    <summary>Create/Update an entry in the dictionary.</summary>
    <remarks>For every word there are deletes with an edit distance of 1..maxEditDistance created and added to the
    dictionary. Every delete entry has a suggestions list, which points to the original term(s) it was created from.
    The dictionary may be dynamically updated (word frequency and new words) at any time by calling CreateDictionaryEntry</remarks>
    <returns>True if the word was added as a new correctly spelled word,
    or False if the word is added as a below threshold word, or updates an
    existing correctly spelled word.</returns>
    '''
    def create_dictionary_entry(self,term,count,max_dictionary_edit_distance=2,prefix_length=7):
        if count < 1:
            if self.count_threshold > 0:
                return False
        # look first in the below threshold words,
        # update count, and allow promotion to correct spelling word if it reaches count
        if self.count_threshold > 1:
            prev_count = self.below_threshold_words.get(term)
            if prev_count:
                new_count = prev_count + count
                if new_count > self.count_threshold:
                    # promote word to correct spellings
                    self.below_threshold_words.pop(term)
                else:
                    # update the count in below threshold words
                    self.below_threshold_words[term] = new_count
                    return False

        else:
            prev_count = self.words.get(term)
            if prev_count:
                # update the count in the word dictionary
                new_count = prev_count + count
                self.words[term] = new_count
                return False
            elif count < self.count_threshold:
                # add the word  to the list of below threshold words
                self.below_threshold_words[term] = count
                return False

        # else the word is new and above the threshold
        self.words[term] = count

        # we'll create the edits and suggestions for this new word
        if len(term) > self.max_dictionary_word_length:
            self.max_dictionary_word_length = len(term)

        # create delete edits
        edits = SymspellDictionary._get_edits_prefix(term,max_dictionary_edit_distance,prefix_length)

        if edits:
            if self.deletes is None:
                self.deletes = dict()
            # iterate over each delete edit
            for delete in edits:

                # get a hash key for the edit
                delete_hash = SymspellDictionary._get_string_hash(delete)

                # add the term to the suggestions for each delete edit
                suggestions = self.deletes.get(delete_hash)
                if suggestions:
                    suggestions.append(term)
                else:
                    suggestions = [term]
                self.deletes[delete_hash] = suggestions

        return True

    '''
    <summary>Create/Update an entry in the dictionary.</summary>
    <remarks>For every word there are deletes with an edit distance of 1..maxEditDistance created and added to the
    dictionary. Every delete entry has a suggestions list, which points to the original term(s) it was created from.
    The dictionary may be dynamically updated (word frequency and new words) at any time by calling CreateDictionaryEntry</remarks>
    <returns>True if the word was added as a new correctly spelled word,
    or false if the word is added as a below threshold word, or updates an
    existing correctly spelled word.</returns>
    '''

    def lookup(self, input, verbosity,max_edit_distance, include_unknown):
        if max_edit_distance > self.max_dictionary_edit_distance:
            logging.error("Invalid edit distance")
            sys.exit(-1)
        suggestions = list()
        input_len = len(input)

        # word is too long to possibly match any suggestions
        if input_len - max_edit_distance > self.max_dictionary_word_length:
            return None

        num_suggestions = 0
        # quick look for an exact match
        suggestion_count = self.words.get(input)
        if suggestion_count:
            suggestion = SymspellSuggestion(input,0,suggestion_count)
            suggestions.append(suggestion)
            return suggestions

        if max_edit_distance == 0:
            return None

        deletes_considered = set()
        suggestions_considered = set()

        # we considered the input as a suggestion
        suggestions_considered.add(input)
        max_edit_distance_candidate = max_edit_distance
        candidate_index = 0
        single_suggestion = ''
        candidates = list()

        # Add original prefix
        input_prefix_len = input_len
        if input_prefix_len > self.prefix_length:
            input_prefix_len = self.prefix_length
            candidates.append(input[:input_prefix_len])
        else:
            candidates.append(input)

        # Use the levenshtein distance
        algorithm = DistanceAlgorithms.DistanceAlgorithms.LEVENSHTEIN
        edit_distance = DistanceAlgorithm.DistanceAlgorithm(algorithm)
        while candidate_index < len(candidates):
            candidate = candidates[candidate_index]
            candidate_index = candidate_index + 1
            candidate_len = len(candidate)
            len_diff = input_prefix_len - candidate_len
            # if candidate distance is already higher than suggestion distance,
            # then there are no better suggestions to be expected
            if len_diff > max_edit_distance_candidate:
                break

            # read candidate entry from the dictionary
            suggestions = self.deletes.get(SymspellDictionary._get_string_hash(candidate))

            if suggestions:
                for suggestion in suggestions:

                    if suggestion == input:
                        continue
                    suggestion_len = len(suggestion)

                    # input and suggestion lengths differ more than the allowed best distance
                    if ((abs(suggestion_len - input_len) > max_edit_distance_candidate) or \
                        # suggestion must be for a different delete string, in same bin only because of hash collision
                        (suggestion_len < candidate_len) or \
                        # if suggestion len = candidate len, then it either equals delete or is in same bin only because of hash collision
                        (suggestion_len == candidate_len and suggestion != candidate)):
                        continue
                    suggestion_prefix_len = min(suggestion_len,self.prefix_length)

                    if suggestion_prefix_len > input_prefix_len and (suggestion_prefix_len - candidate_len) > max_edit_distance_candidate:
                        continue

                    '''
                    True Damerau-Levenshtein Edit Distance: adjust distance, if both distances>0
                    We allow simultaneous edits (deletes) of maxEditDistance on on both the dictionary and the input term. 
                    For replaces and adjacent transposes the resulting edit distance stays <= maxEditDistance.
                    For inserts and deletes the resulting edit distance might exceed maxEditDistance.
                    To prevent suggestions of a higher edit distance, we need to calculate the resulting edit distance, if there are simultaneous edits on both sides.
                    Example: (bank==bnak and bank==bink, but bank!=kanb and bank!=xban and bank!=baxn for maxEditDistance=1)
                    Two deletes on each side of a pair makes them all equal, but the first two pairs have edit distance=1, the others edit distance=2.
                    '''
                    distance = 0
                    min = 0
                    if candidate_len == 0:
                        distance = max(input_len,suggestion_len)
                        if distance > max_edit_distance_candidate:
                            continue
                        if suggestion in suggestions_considered:
                            continue
                        suggestions_considered.add(suggestion)

                    elif suggestion_len == 1:
                        if input.find(suggestion[:1]) < 0:
                            distance = input_len
                        else:
                            distance = input_len - 1
                        if distance > max_edit_distance_candidate:
                            continue
                        if suggestion in suggestions_considered:
                            continue
                        suggestions_considered.add(suggestion)
                    else:
                        '''
                        number of edits in prefix ==maxediddistance  AND no identic suffix,
                        then editdistance>maxEditDistance and no need for Levenshtein calculation  
                        (input_len >= prefix_len) && (suggestion_len >= prefix_len)
                        '''
                        is_candidate_len = self.prefix_len - max_edit_distance == candidate_len
                        min_len = min(input_len,suggestion_len)

                        #TODO: Check this logic
                        input_suggestion_test_1 = input[input_len + 1 - min_len:] != suggestion[suggestion_len + 1 - min_len]
                        input_suggestion_test_2 = min_len > 0 and (input[input_len - min] != suggestion[suggestion_len - min])
                        input_suggestion_test_3 = input[input_len - min - 1 ] != suggestion[suggestion_len - min]
                        input_suggestion_test_4 = input[input_len - min] != suggestion[suggestion_len - min - 1]

                        if is_candidate_len and ( min_len > 1 and (input_suggestion_test_1 or input_suggestion_test_2) and (input_suggestion_test_3 or input_suggestion_test_4)):
                            continue
                        else:
                            # Delete In Suggestion Prefix is expensive computation
                            # Only use it when verbosity is Top or Closest
                            if verbosity is SymspellVerbosity.TOP or verbosity is SymspellVerbosity.CLOSEST:
                                #TODO: Complete impl
                                pass
                    # Do not process higher distances than those
                    # already found if verbosity is not ALL.
                    # In that case, maxEditDistanceCandidate is equal to the maxEdiDistance

                    if  distance < max_edit_distance_candidate:
                        suggestion_count = self.words[suggestion]
                        symspell_suggestion = SymspellSuggestion(suggestion,distance,suggestion_count)
                        
                        if suggestion_count > 0:

                            # If verbosity is closest, calcute the DemLev distance only up ot the smallest found distance so far
                            if verbosity is SymspellVerbosity.CLOSEST:
                                if distance < max_edit_distance_candidate:
                                    suggestions = []
                            elif verbosity is SymspellVerbosity.TOP:
                                if distance < max_edit_distance_candidate or suggestion_count > suggestions[0].count:
                                    max_edit_distance_candidate = distance
                                    suggestions[0] = symspell_suggestion
                                continue
                        if verbosity is SymspellVerbosity.ALL:
                            max_edit_distance_candidate = distance
                        suggestions.append(symspell_suggestion)

                            #
            # add edits
            # derive edits from the input and add to the candidate list recursively
            if len_diff < max_edit_distance and candidate_len <= self.prefix_length:
                # don't need to create edits with edit distance smaller than the suggestions already found
                if verbosity is not SymspellVerbosity.ALL and len_diff > max_edit_distance_candidate:
                    continue

                for i in range(candidate_len):
                    delete = candidate[0:i] + candidate[i+1:]
                    if delete not in deletes_considered:
                        deletes_considered.add(delete)
                        candidates.append(delete)
            
        # sort by ascending edit distance
        if len(suggestions) > 1:
            suggestions = _sort_suggestions(suggestions)
            if include_unknown is True and len(suggestions) == 0:
                suggestions.add(SymspellSuggestion(input,max_edit_distance+1,0))
        return suggestions




















