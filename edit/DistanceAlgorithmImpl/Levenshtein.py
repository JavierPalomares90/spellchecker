# Copyright (C) 2020 Javier Palomares

import numpy as np
import Levenshtein as lev

# Implemenation of levenshtein distance
class Levenshtein(DistanceAlgorithm):
    def edit_distance(self, str1, str2):
        #TODO: Need to figure out how to include the ratios in here
        return lev.distance(str1,str2)