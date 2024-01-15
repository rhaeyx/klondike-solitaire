class Card:
    def __init__(self, suit, rank, up = False):
        self.suit = suit
        self.rank = rank
        self.up = up
        
    def value(self):
        return self.suit + self.rank
            
    def __repr__(self):
        if self.up:
            return self.value()
        return '[]'