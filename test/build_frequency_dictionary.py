#!/usr/bin/env python3
# Copyright (C) 2020 Javier Palomares

import argparse
import os.path
from os import path

def get_args():
    parser = argparse.ArgumentParser(description="Build dictionary from a master list")
    parser.add_argument("-m","--master_list",required=True, help="The master list to use")
    parser.add_argument("-s","--save_path",required=True, help="Where to save the dictionary to")
    args = parser.parse_args()
    return args

def load_dictionary(master_list_text,separator):
    dictionary = dict()
    line = master_list_text.readline()
    token_frequency = 0
    while line:
        # get all the tokens in the list
        tokens = line.rstrip().split(separator)
        for i in range(len(tokens)):
            token = tokens[i]
            count = dictionary.get(token)
            if count is None:
                count = 0
            dictionary[token] = count+1
            token_frequency = token_frequency + 1
        line = master_list_text.readline()
    return dictionary,token_frequency

def write_dictionary(dictionary, frequency_count, save_path):
    with open(save_path,'w',encoding="utf-8") as save_file:
        save_file.write('{}'.format(frequency_count))
        for key,value in dictionary.items():
            save_file.write('{key} {value}\n'.format(key=key,value=value))
    


def build_dictionary(master_list,save_path):
    if path.exists(master_list) == False:
        logging.error("Master list {} does not exist".format(master_list))
        sys.exit(-1)
    with open(master_list, 'r', encoding="utf-8") as master_list_text:
        dictionary,frequency_count = load_dictionary(master_list_text, ' ')
    write_dictionary(dictionary,frequency_count,save_path)

    


def main():
    args = get_args()
    master_list = args.master_list
    save_path = args.save_path
    build_dictionary(master_list,save_path)


if __name__ == '__main__':
    main()

