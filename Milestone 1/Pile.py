class Pile:
    def __init__(self, cards):
        self.cards = cards
        self.cards[-1].up = True # set top most card up
        
    def __len__(self):
        return len(self.cards)
    
    def isEmpty(self):
        return len(self.cards) == 0

    def get_card_by_value(self, value):
        for card in self.cards:
            if card.value() == value:
                return card
        return '[]'
            
    def get_card_by_index(self, index):
        return self.cards[index]
        
    def get_cards(self):
        return self.cards
    
    def pop_card(self, card):
        index = self.cards.index(card)
        card = self.cards[index:]
        self.cards = self.cards[:index]
        if not self.isEmpty():
            if not self.cards[-1].up:
                self.cards[-1].up = True
        return card
    
    def add_card(self, card):
        self.cards.append(card)
        