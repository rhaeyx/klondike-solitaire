class Foundation:
    def __init__(self):
        self.cards = []
    
    def __repr__(self):
        if self.cards: # is not empty
            return str(self.cards[-1]) # return card on top
        return 'XX'
    
    def isEmpty(self):
        return len(self.cards) == 0
    
    def get_cards(self):
        return self.cards
    
    def get_card_by_index(self, index):
        return self.cards[index]
    
    def get_card_by_value(self, value):
        for card in self.cards:
            if card.value() == value:
                return card
        return '[]'

    
    def add_card(self, card):
        self.cards.append(card)
        
    def pop_card(self, card):
        index = self.cards.index(card)
        card = self.cards[index:]
        self.cards = self.cards[:index]
        return card
