# Copyright (C) 2020 Javier Palomares

from enum import Enum

class DistanceAlgorithms(Enum):
    LEVENSHTEIN = 0  #: Levenshtein algorithm.
    DAMERUAUOSA = 1  #: Damerau optimal string alignment algorithm
