# Copyright (C) 2020 Javier Palomares


class SymspellSuggestion:

    def __init__(self, term=None, distance=None, count=None):
        self.term = term
        self.distance = distance
        self.count = count
    
    def __eq__(self,other):
        if other is None:
            if self is None:
                return True
            else:
                return False
        if not isinstance(other,SymspellSuggestion):
            return False
        if self.distance != other.distance:
            return False
        if self.count != other.count:
            return False
        return True

    # < comparison for symspell suggestions. Order by distance, then by frequency
    def __lt__(self,other):
        if self.distance < other.distance:
            return True
        elif self.distance > other.distance:
            return False
        # distances are equal compare by count
        else:
            return self.count > other.count
        
    def __le__(self,other):
        return __eq__(self,other) or __lt__(self,other) 

    def __gt__(self,other):
        return (not __lt__(self,other)) and (not __eq__(self,other))

    def __ge__(self,other):
        return __eq__(self,other) or __gt__(self,other) 

    def __str__(self):
        to_string = "term:{} distance:{} count:{}".format(self.term,self.distance,self.count)
        return to_string

