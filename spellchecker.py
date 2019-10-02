#
import argparse


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
    

if __name__ == '__main__':
    main()