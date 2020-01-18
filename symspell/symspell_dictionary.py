# Copyright Javier Palomares 2020


class symspell_dictionary:

    def __init__(self,count_threshold = 3):
        self.count_threshold= count_threshold
        self.max_dictionary_word_length = 0

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

    @staticmethod
    def _get_edits(word,edit_distance,words_set,max_dictionary_edit_distance):
        # delete edits only
        edit_distance += 1
        word_len = len(word)
        if word_len > 1:
            for i in range(word_len):
                # remove the ith character from the word
                delete_edit = word[:i] + word[i+1:]
                if delete_edit in words_set == False:
                    words_set.add(delete_edit)
                    # recursive find other delete edits
                    if edit_distance < max_dictionary_edit_distance:
                        symspell_dictionary._get_edits(delete_edit,edit_distance,words_set,max_dictionary_edit_distance)
        return words_set


    @staticmethod
    def _get_edits_prefix(term,max_dictionary_edit_distance,prefix_length):
        edits = {}
        if len(term) <= max_dictionary_edit_distance:
            # word is too short, add empty string
            edits.add("")
        if len(term) > prefix_length:
            term = term[0:prefix_length]
        edits.add(term)
        return symspell_dictionary._get_edits(term,0,edits,max_dictionary_edit_distance)

    def create_dictionary_entry(self,term,count,max_dictionary_edit_distance,prefix_length):
        if count < 0:
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
        edits = symspell_dictionary._get_edits_prefix(term,max_dictionary_edit_distance,prefix_length)

        #TODO: Complete impl
