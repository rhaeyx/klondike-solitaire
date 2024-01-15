#!/usr/bin/python3

import random
import os

from Pile import Pile
from Foundation import Foundation
from Stock import Stock
from Card import Card

class KlondikeSolitaire():    
    # initialize game
    def __init__(self):
        self.debug = False
        
        self.save_file = 'save.txt'
        
        self.foundationLabels = ['A', 'B', 'C', 'D']
        self.suits = ['H', 'D', 's', 'c']
        self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        
        # 4 foundations
        self.foundations = [Foundation(), Foundation(), Foundation(), Foundation()]

        deck = self.generate_deck()
        if self.debug:
            random.seed(5)
        random.shuffle(deck)
        
        # deal cards to piles
        self.piles = []
        for i in range(7):
            pile = []
            for _ in range(i + 1):
                pile.append(deck.pop())
            self.piles.append(Pile(pile))
            
        # whats left is now in stock                
        self.stock = Stock(deck)
        
        self.message = '[^_^] Welcome to Solitaire!'
        self.main()

    def show_game(self, piles, foundations, stock, message):
        output = ''
        output += 'S O L I T A I R E\n\n\n'
        
        # add stock
        output += f'S: {stock}\t'
        
        # add foundations 
        for label, foundation in zip(['A', 'B', 'C', 'D'], foundations):
            output += f'\t{label}:{foundation}'
        output += '\n\n\n'
        
        # add pile column labels
        for i in range(1, 8):
            output += f'{str(i)}:\t'
        output += '\n'
        
        # add pile cards    
        longest_pile = max([len(pile) for pile in piles])
        for i in range(longest_pile):
            for pile in piles:
                if i < len(pile): # if pile still has cards
                    card = pile.get_card_by_index(i)
                    output += f'{card.value() if card.up else "[]" }\t'
                else: 
                    output += '\t'
            output += '\n'
        output += '\n'
        
        output += ' [1] Move\n'
        output += ' [2] Deal\n'
        output += ' [3] Save Game\n'
        output += ' [4] Load Game\n'
        output += ' [CTRL+C] Exit\n'
        if message:
            output += f' {message}\n'
        else: 
            output += '\n'

        if not self.debug:
            os.system('cls||clear')
        self.printDebug()
        print(output, end='')
        
        
    # generate all cards in a deck and put in a list
    def generate_deck(self):
        # cards are 2 chars, suit + rank
        deck = []
        for suit in self.suits:
            for rank in self.ranks:
                card = Card(suit, rank)
                deck.append(card)
        return deck
    
    def isValidMove(self, card, source, target, cardFrom, cardTo):
        # from pile
        if cardFrom == 'P':
            cards = source.get_cards_from_card(card)
            for c in cards:
                if not c.up:
                    self.message = '[ERROR] All cards must be facing up.'
                    return False
        
        # to pile
        if cardTo == 'P':
            if target.isEmpty(): # card must be king
                if card.rank != 'K':
                    self.message = '[ERROR] Only a king can be added to an empty pile.'
                    return False
                
            else:
                lastCard = target.get_card_by_index(-1)
                # check suits
                if (str(card)[0].islower() == str(lastCard)[0].islower()): # if both are lowercase or both uppercase
                    self.message = '[ERROR] Color of the suits must be different.'
                    return False
                
                # check rank
                if self.ranks.index(lastCard.rank) - self.ranks.index(card.rank) != 1:
                    self.message = '[ERROR] Target pile\'s last card must be the next direct rank of card.'
                    return False
        
        # to foundation
        if cardTo == 'F': 
            if target.isEmpty():
                if not card.value().endswith('A'):
                    self.message = '[ERROR] You can only start a foundation with an Ace.'
                    return False
            else:
                lastCard = target.get_card_by_index(-1)
                if str(card)[0] != str(lastCard)[0]: # should have the same suit
                    self.message = '[ERROR] You can only add a card of the same suit to the foundation.'
                    return False            
        
        return True
    
    def move_card(self):
        # validate
        try:
            source = None
            moveCard = None
            
            # determine where the source of the card
            cardSource = input(' Move FROM Stock(S), Pile(P), Foundation(F): ').upper()
            if cardSource == 'S':
                source = self.stock
            elif cardSource == 'P':
                sourcePile = int(input(' Input pile # (1-7): '))
                if sourcePile < 1 or sourcePile > 7:
                    self.message = '[ERROR] Invalid input. Try again with a number from 1 to 7.'
                    return
                source = self.piles[sourcePile - 1]
            elif cardSource == 'F':
                sourceFoundation = input(' Input foundation label (A-D): ').upper()
                if sourceFoundation not in self.foundationLabels:
                    self.message = '[ERROR] Invalid input. Try again with a character from A to D.'
                    return
                source = self.foundations[self.foundationLabels.index(sourceFoundation)]
            else: 
                self.message = '[ERROR] Invalid input.'
                return

            # determine which card
            moveCardInput = input(' Move which CARD (eg. c7): ')        
            moveCard = source.get_card_by_value(moveCardInput)
            if moveCard == '[]' or not moveCard.up:
                self.message = f'[ERROR] Card {moveCardInput} not found in {"Stock" if cardSource == "S" else "Pile #" + str(sourcePile)}'
                return
            
            # determine where to place the card
            cardTarget = input(' Move TO Foundation(F) or Pile(P): ').upper()
            if cardTarget == 'F':
                targetFoundation = input(' Input foundation label (A-D): ').upper()
                if targetFoundation not in self.foundationLabels:
                    self.message = '[ERROR] Invalid input. Try again with a character from A to D.'
                    return
                target = self.foundations[self.foundationLabels.index(targetFoundation)]
            elif cardTarget == 'P': 
                targetPile = int(input(' Input pile # (1-7): '))
                if targetPile < 1 or targetPile > 7:
                    self.message = '[ERROR] Invalid input. Try again with a number from 1 to 7.'
                    return
                target = self.piles[targetPile - 1]
            else: 
                self.message = '[ERROR] Invalid input.'
                return
                
                
            # check if valid move
            if not self.isValidMove(moveCard, source, target, cardSource, cardTarget):
                return 
            
            # get card from source
            moveCards = []
            if cardSource == 'P':
                moveCards = source.pop_card(moveCard) # move multiple cards if from pile
            elif cardSource == 'S' or cardSource == 'F':
                moveCards = source.pop_card(moveCard) # move only one card if from stock or foundation
                
            # add cards to target
            if cardTarget == 'P':
                target.add_cards(moveCards)
            elif cardTarget == 'S' or cardTarget == 'F':
                target.add_card(moveCard) # move only one card if adding to stock or foundation
            
        except KeyboardInterrupt:
            print('\n Bye bye!')
            exit()
        # except Exception as e:
        #     self.message = '[ERROR] Something went wrong.'
        #     return
      
    def save_state(self):
        state = self.generate_state()
        
        with open(self.save_file, 'w') as f:
            f.write(state)
            
        self.message = f'[SAVED] Game state saved in {self.save_file}'
              
    def generate_state(self):
        state = ""
        
        # stock: n_stock stocks 
        if len(self.stock) != 0:
            state += f'{len(self.stock)} {" ".join([str(card) for card in self.stock.get_cards()])} {str(self.stock)}\n'
        else: 
            state += '0\n'
        
        # foundations: a b c d
        state += f'{" ".join([str(card) for card in self.foundations])}\n'
        
        # piles: 1 to 7
        for pile in self.piles:
            if len(pile) != 0:
                state += f'{len(pile)} {" ".join([str(card.value()) for card in pile.get_cards()])} {len(pile.get_up_cards())}\n'
            else:
                state += '0\n'
        
        return state
    
    def load_state(self):
        state = ''
        
        with open(self.save_file, 'r') as f:
            state = ''.join(f.readlines())
            
        self.apply_state(state)
        
        self.message = '[LOADED] Previously saved game has been loaded.'
    
    def apply_state(self, state):
        lines = state.strip().split('\n')
        print(lines)
        
        # stock
        stockLine = lines.pop(0)
        if stockLine.startswith('0'):
            self.stock = Stock([])
        else:
            tokens = stockLine.split(' ')
            n_stock = int(tokens.pop(0))
            cards = []
            for _ in range(n_stock):
                n_stock_i = tokens.pop(0)
                cards.append(Card(n_stock_i[0], n_stock_i[1]))
            self.stock = Stock(cards)
            current_card = tokens.pop(0)
            self.stock.set_current_index_by_card(Card(current_card[0], current_card[1], up=True))
            
        # foundation
        foundationLine = lines.pop(0)
        tokens = foundationLine.split(' ')
        self.foundations = []
        for token in tokens:
            foundation = Foundation()
            if token == 'XX':
                self.foundations.append(foundation)
                continue
            suit = token[0]
            rank = token[1]
            for r in self.ranks:
                foundation.add_card(Card(suit, r, up=True))
                if rank == r:
                    break
            self.foundations.append(foundation)
            
        # piles
        self.piles = []
        for pileLine in lines:
            if pileLine.startswith('0'):
                self.piles.append(Pile([]))
                continue
            tokens = pileLine.split(' ')
            n_pile = int(tokens.pop(0))
            cards = []
            for _ in range(n_pile):
                current_card = tokens.pop(0)
                cards.append(Card(current_card[0], current_card[1]))
            pile = Pile(cards)
            up_cards = int(tokens.pop(0))
            pile.set_up_cards(up_cards)
            self.piles.append(pile)


        
            

    def printDebug(self):
        if self.debug:
            print('=' * 29 + 'DEBUG' + '=' * 30)
            print('PILES: ')
            for i, pile in enumerate(self.piles):
                print(i, i+1, ' '.join([card.value() for card in pile.get_cards()]))
                
            print('STOCK: ', self.stock)
            print(' '.join([card.value() for card in self.stock.get_cards()]))
            
            print('FOUNDATIONS: ')
            abcd = 'ABCD'
            for i, foundation in enumerate(self.foundations):
                print(i, abcd[i], ' '.join([card.value() for card in foundation.get_cards()]))
            print('=' * 64)

    def main(self):
        try:
            while True:
                self.show_game(self.piles, self.foundations, self.stock, self.message)
                self.message = ''
                                
                choice = input(' Enter choice: ')
                
                if choice == '1': # move
                    self.move_card()
                elif choice == '2': # deal
                    self.stock.deal()
                elif choice == '3': # save state
                    self.save_state() 
                elif choice == '4': # load state
                    self.load_state() 
                else:
                    self.message = '[ERROR] Invalid choice!'
        except KeyboardInterrupt:
            print('\n Bye bye!')
            exit()

if __name__ == "__main__":
    game = KlondikeSolitaire()
    game.main()