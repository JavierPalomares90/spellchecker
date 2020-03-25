#!/usr/bin/env python3
# Copyright (C) 2020 Javier Palomares

from symspell import symspell,SymspellDictionary,SymspellVerbosity
from norvig import norvig
import time

def get_symspell_suggestions(dictionary,tokens):
    s = ''
    start_time = time.time()
    for t in tokens:
        sg = dictionary.lookup(t,verbosity=SymspellVerbosity.SymspellVerbosity.TOP,max_edit_distance=2,include_unknown=False)
        if len(sg) > 0:
            s += " " + sg[0].term
    end_time = time.time()
    return s, end_time - start_time
    
def get_bigram_suggestions(input_term,bigram_dictionary):
    s = ''
    start_time = time.time()
    suggestions = bigram_dictionary.lookup_compound(input_term, max_edit_distance=2)
    end_time = time.time()
    for suggestion in suggestions:
        s += suggestion.term
    return s, end_time - start_time

def get_norvig_suggestions(tokens,dictionary_terms,error_model):
    s = ''
    start_time = time.time()
    max_edit_distance =2
    for t in tokens:
        correction = norvig.get_spelling_correction(t,dictionary_terms,error_model,max_edit_distance)
        if correction is not None:
            s += ' ' + correction
    end_time = time.time()
    return s, end_time - start_time



def run_scenario_i(dictionary,bigram,norvig_dict,norvig_error_model,i):
    scenario1_file = "resources/data/scenarios/scenario{}.txt".format(i)
    result_file = "resources/data/scenarios/results/scenario{}_result.txt".format(i)
    r = open(result_file,'w+')
    with open(scenario1_file,'r',encoding='utf-8') as test_file_text:
        line = test_file_text.readline()
        r.write("Input, Sympell suggestion,Symspell Exec time(seconds),Bigram suggestion,Bigram Exec time (seconds),Norvig suggestion, Norvig exec time\n")
        while line:
            try:
                tokens = line.split(' ')
                symspell_suggestions,symspell_execution_time = get_symspell_suggestions(dictionary,tokens)
                bigram_suggestions,bigram_execution_time = get_bigram_suggestions(line,bigram)
                norvig_suggestions, norvig_execution_time = get_norvig_suggestions(tokens,norvig_dict,norvig_error_model)
                r.write('{input},{symspell},{symspell_exec},{bigram},{bigram_exec},{norvig},{norvig_exec}\n'
                .format(input=line.strip(),symspell=symspell_suggestions,symspell_exec=symspell_execution_time,bigram=bigram_suggestions,
                bigram_exec=bigram_execution_time,norvig=norvig_suggestions,norvig_exec=norvig_execution_time))
                line = test_file_text.readline()
            except:
                line = test_file_text.readline()
                continue
    r.close()

def main():
    dictionary_path = "resources/data/freq_dict.txt"
    bigram_path = "resources/data/bigram_dict.txt"
    master_list = "resources/data/master_list.txt"
    corpus_size = 19684
    dictionary = symspell.load_dictionary(dictionary_path)
    bigram_dictionary = symspell.load_bi_gram_dictionary(bigram_path,corpus_size,dictionary=dictionary)
    norvig_dict, norvig_error_model = norvig.get_error_model(master_list)
    scenarios = ['1','2','3','4','5','5_2','5_3','6','8','9','10']
    for i in scenarios:
        run_scenario_i(dictionary,bigram_dictionary,norvig_dict,norvig_error_model,i)

if __name__ == '__main__':
    main()