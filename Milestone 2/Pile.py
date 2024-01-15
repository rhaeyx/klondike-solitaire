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

    def get_up_cards(self):
        up_cards = []
        for card in self.cards[::-1]:
            if card.up:
                up_cards.append(card)
                continue
            break
        return up_cards

    def set_up_cards(self, n):
        for card in self.cards[::-1]:
            if n != 0:
                card.up = True
                n -= 1
                continue
            break
    
    def get_cards_from_card(self, card):
        # checks if all cards after the specified card is up
        index = self.cards.index(card)
        return self.cards[index:]
        
    def pop_card(self, card):
        index = self.cards.index(card)
        cards = self.cards[index:]
        self.cards = self.cards[:index]
        if not self.isEmpty():
            if not self.cards[-1].up:
                self.cards[-1].up = True
        return cards
    
    def add_cards(self, cards):
        for card in cards:
            self.cards.append(card)
        
        