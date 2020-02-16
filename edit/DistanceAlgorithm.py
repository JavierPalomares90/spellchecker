# Copyright (C) 2020 Javier Palomares


from .DistanceAlgorithms import DistanceAlgorithms
from .DistanceAlgorithmImpl import Levenshtein
from .DistanceAlgorithmImpl import Damerauosa

'''
Interface method for distance algos implementation
'''
class DistanceAlgorithm(object):
    def __init__(self,distance_algo):
        # the distance algorithm to use
        self.algorithm = distance_algo 
        if distance_algo == DistanceAlgorithms.LEVENSHTEIN:
            self._distance_comparer = Levenshtein()
        elif distance_algo == DistanceAlgorithms.DAMERUAUOSA:
            self._distance_comparer = Damerauosa()
        else:
            raise ValueError("Unknown distance algorithm")

    def edit_distance(self, string_1, string_2):
        raise NotImplementedError("Do not use this interface class. You must extend this class.")

    def get_distance(self, string_1, string_2):
        return self.edit_distance(string_1,string_2)
