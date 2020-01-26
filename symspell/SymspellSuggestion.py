# Copyright Javier Palomares 2020


class SymspellSuggestion:

    def __init__(self):
        self.Term = None
        self.distance = None
        self.count = None

    def __init__(self, term, distance, count):
        self.term = term
        self.distance = distance
        self.count = count

