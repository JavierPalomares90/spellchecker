#
import argparse
import Levenshtein as lev
import sys
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 


def parse_args():
    parser = argparse.ArgumentParser(description='Read the master list')
    parser.add_argument('-p','--path')
    args = parser.parse_args()
    return args

# Read the master list line by line
def read_master_list(path):
    master_list = []
    with open(path,'r') as fp:
        line = fp.readline()
        while line:
            line = line.rstrip('\n')
            master_list.append(line)
            line = fp.readline()
    return master_list 

def main():
    args = parse_args()
    master_list_path = args.path
    choices = read_master_list(master_list_path)
    while True:
        query = input("What are you looking for?\n").lower()
        # Compute the best choice using the leveshtein distance and WRatio
        #print("Using token set ratio")
        #print(process.extract(query,choices,scorer=fuzz.token_set_ratio))
        #print("Using partial token set ratio")
        #print(process.extract(query,choices,scorer=fuzz.partial_token_set_ratio))
        #print("Using partial ratio")
        #print(process.extract(query,choices,scorer=fuzz.partial_ratio))
        best = process.extractOne(query,choices, scorer=fuzz.token_sort_ratio)
        print("I think you meant: {}".format(best))


    

if __name__ == '__main__':
    main()
