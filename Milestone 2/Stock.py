class Stock:
    def __init__(self, cards):
        self.cards = cards
        for card in self.cards:
            card.up = True
        self.index = len(cards) - 1
        
    def __len__(self):
        return len(self.cards)
            
    def __repr__(self):
        if self.index == len(self.cards) - 1:
            return '[]'
        
        if self.cards: # is not empty
            return str(self.cards[self.index + 1].value()) # return card on top
        
        return 'XX'
    
    def set_current_index_by_card(self, card): 
        for i, c in enumerate(self.cards):
            if c.value() == card.value():
                self.index = i - 1
                break
    
    def isEmpty(self):
        return len(self.cards) == 0
    
    def get_cards(self):
        return self.cards
    
    def get_card_by_index(self, index):
        return self.cards[index + 1]
    
    def get_card_by_value(self, value):
        for i, card in enumerate(self.cards):
            if card.value() == value and i == self.index + 1:
                return card
        return '[]'
    
    def pop_card(self, card):
        index = self.cards.index(card)
        card = self.cards[index:index+1]
        self.cards = self.cards[:index] + self.cards[index+1:]
        return card
    
    def deal(self):            
        if self.index < 0: # if theres no more cards
            self.index = len(self.cards) - 1 # reset to last card
        else:    
            self.index -= 1
