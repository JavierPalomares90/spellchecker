# Copyright (C) 2020 Javier Palomares


class SymspellSuggestion:

    def __init__(self):
        self.term = None
        self.distance = None
        self.count = None

    def __init__(self, term, distance, count):
        self.term = term
        self.distance = distance
        self.count = count

