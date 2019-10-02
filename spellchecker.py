#
import argparse
import Levenshtein as lev
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='Read the master list')
    parser.add_argument('-p','--path')
    args = parser.parse_args
    return args

# Read the master list line by line
def read_master_list(path):
    master_list = []
    with open(path,'r') as fp:
        line = fp.readline()
        while line:
            master_list.append(line)
    return line

def main():
    args = parse_args()
    master_list_path = args.path
    master_list = read_master_list(master_list_path)
    while True:
        user_input = input("What are you looking for?").lower()
        # Compute the leveshtein distance 
        best_distance = sys.maxint
        best_ratio = 0
        best_option = None
        for string in master_list:
            d = lev.distance(user_input,string.lower())
            r = lev.ratio(user_input,string.lower())
            if (d < best_distance):
                best_distance = d
                best_ration = r
                best_option = string
        print("I think you meant: {}".format(best_option))


    

if __name__ == '__main__':
    main()
