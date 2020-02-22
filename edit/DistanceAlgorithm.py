# Copyright (C) 2020 Javier Palomares

import numpy as np
import Levenshtein as lev
from .DistanceAlgorithms import DistanceAlgorithms

'''
Interface method for distance algos implementation
'''
class DistanceAlgorithm():
    def __init__(self,distance_algorithm):
        # the distance algorithm to use
        self.algorithm = distance_algorithm
        if self.algorithm == DistanceAlgorithms.LEVENSHTEIN:
            self._distance_comparer = Levenshtein()
        elif self.algorithm == DistanceAlgorithms.DAMERUAUOSA:
            self._distance_comparer = Damerauosa()
        else:
            raise ValueError("Unknown distance algorithm")

    def edit_distance(self, string1, string2):
        return self._distance_comparer.edit_distance(string1,string2)

    def get_distance(self, string1, string2):
        return self.edit_distance(string1,string2)

# Implemenation of levenshtein distance
class Levenshtein():
    def edit_distance(self, str1, str2):
        #TODO: Need to figure out how to include the ratios in here
        return lev.distance(str1,str2)

# 
class Damerauosa(DistanceAlgorithm):
    def edit_distance(self, str1, str2):
        #TODO: Complete impl
        return 0

class Fuzzy(DistanceAlgorithm):
    def edit_distance(self, str1, str2):
        '''
        query = input("What are you looking for?\n").lower()
         Compute the best choice using the leveshtein distance and WRatio
        print("Using token set ratio")
        print(process.extract(query,choices,scorer=fuzz.token_set_ratio))
        print("Using partial token set ratio")
        print(process.extract(query,choices,scorer=fuzz.partial_token_set_ratio))
        print("Using partial ratio")
        print(process.extract(query,choices,scorer=fuzz.partial_ratio))
        best = process.extractOne(query,choices, scorer=fuzz.token_sort_ratio)
        print("I think you meant: {}".format(best))
        '''
        #TODO: Complete impl
        return 0
