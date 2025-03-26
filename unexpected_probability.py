"""
This script creates the Unexpected and Probability cards that players can draw during the game.

The main attributes are:

    index: Acts as a pointer, indicating which card from the deck will be drawn next.
           It keeps track of the current position, incrementing every time a card is drawn.

    dictionary: Contains the following keys:
        text: The description of the card's content.
        stonks: Indicates whether the card represents a positive situation (stonks) or a negative one (not stonks).
        position: If present, specifies a new position the player must move to.

The main methods are:

    shuffle: Shuffles the deck at the beginning of the game and reshuffles it whenever all the cards have been drawn,
             as long as the game is not over.

    draws_card_u or draws_card_p: Allow the player who lands on an Unexpected or Probability space
                                  to draw a card from the respective deck.

Written by: Roberto Parodo
"""

import random

class Unexpected(object):
    def __init__(self):
        self.index = -1
        self.unexpected_card = [
            {"text": "Andate fino al Parco Della Vittoria se passate dal VIA! ritirate 200 €", "stonks": False, "not_stonks": False, "new_position": 39},
            {"text": "Andate fino alla Stazione ferroviaria più vicina: se è libera potete acquistarla dalla banca; se è posseduta da un altro giocatore, pagate al proprietario il doppio dell'affitto che gli spetta normalmente", "stonks": False, "not_stonks": 2, "new_position": False},
            {"text": "Multa per eccesso di velocità: pagate 15 €", "stonks": False, "not_stonks": 15, "new_position": False},
            {"text": "Andate sino a Corso Ateneo: se passate dal VIA! ritirate 200 €", "stonks": False, "not_stonks": False, "new_position": 13},
            {"text": "Andate sino a Largo Colombo: se passate dal VIA! ritirate 200 €", "stonks": False, "not_stonks": False, "new_position": 24},
            {"text": "Andate fino alla Stazione ferroviaria più vicina: se è libera potete acquistarla dalla banca; se è posseduta da un altro giocatore, pagate al proprietario il doppio dell'affitto che gli spetta normalmente", "stonks": False, "not_stonks": 2, "new_position": False},
            {"text": "Fate 3 passi indietro (con tanti auguri!)", "stonks": False, "not_stonks": False, "new_position": -3},
            {"text": "Maturano le cedole dei vostri fondi immobiliari: incassate 150 €", "stonks": 150, "not_stonks": False, "new_position": False},
            {"text": "Siete stati promossi alla presidenza del consiglio di amministrazione: pagate 50 € alla banca", "stonks": False, "not_stonks": 50, "new_position": False},
            {"text": "La banca vi paga un dividendo di 50 €", "stonks": 50, "not_stonks": False, "new_position": False},
            {"text": "Andate in prigione direttamente e senza passare dal VIA!", "stonks": False, "not_stonks": False, "new_position": 30},
            {"text": "Eseguite lavori di manutenzione su tutti i vostri edifici: pagate 25 € per ogni casa e 100 € per ogni albergo che possedete", "stonks": False, "not_stonks": 25, "new_position": False},
            {"text": "Andate alla Stazione Nord: se passate dal VIA! ritirate 200 €", "stonks": False, "not_stonks": False, "new_position": 25},
            {"text": "Avanzate fino alla Società più vicina: se è libera potete acquistarla dalla banca; se è posseduta da un altro giocatore, pagate al proprietario 10 volte il totale uscito sui dadi", "stonks": False, "not_stonks": 10, "new_position": False},
            {"text": "Andate avanti fino al VIA! e ritirate 200 €", "stonks": 200, "not_stonks": False, "new_position": -1},
        ]

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.unexpected_card)

    def draws_card_u(self) -> dict:
        # If, during the game, all the cards have been drawn, the deck is reshuffled, and the process restarts from index -1, meaning the first card of the deck.
        if self.index >= 14:
            self.index = -1
            self.shuffle()
        self.index += 1
        return self.unexpected_card[self.index]

class Probability(object):
    def __init__(self):
        self.index = -1
        self.probability_card = [
            {"text": "Avete Vinto il secondo premio in un concorso di bellezza! incassate 10 €", "stonks": 10, "not_stonks": False, "new_position":False},
            {"text": "La banca riconosce un errore nel vostro estratto conto: incassate 200 €", "stonks": 200, "not_stonks": False, "new_position":False},
            {"text": "Andate avanti fino al VIA e ritirate 200 €", "stonks": 200, "not_stonks": False, "new_position":-1},
            {"text": "Ereditate 100 € da un lontano zio", "stonks": 100, "not_stonks": False, "new_position":False},
            {"text": "Pagate per contributi di miglioria stradale 40 € per ogni casa e 115 € per ogni albergo che possedete", "stonks": False, "not_stonks": 40, "new_position":False},
            {"text": "Pagate la retta ospedaliera di 100 €", "stonks": False, "not_stonks": 100, "new_position":False},
            {"text": "Pagate le rette scolastiche dei vostri figli: versate 50 €", "stonks": False, "not_stonks": 50, "new_position": False},
            {"text": "Ricevete 25 € per la vostra consulenza", "stonks": 25, "not_stonks": False, "new_position": False},
            {"text": "Maturano le cedole delle vostre azioni: ricevete 100 €", "stonks": 100, "not_stonks": False, "new_position": False},
            {"text": "E' il vostro compleanno: la banca vi regala 10 €", "stonks": 10, "not_stonks": False, "new_position": False},
            {"text": "Vi viene rimborsata la tassa sui redditi: incassate 20 €", "stonks": 20, "not_stonks": False, "new_position": False},
            {"text": "Dalla vendita di uno stock di merci ricavate 50 €", "stonks": 50, "not_stonks": False, "new_position": False},
            {"text": "Ricevete la parcella del dottore pagate 50 €", "stonks": False, "not_stonks": 50, "new_position": False},
            {"text": "Andate in prigione direttamente e senza passare dal VIA!", "stonks": False, "not_stonks": False, "new_position": 10},
            {"text": "Maturano gli interessi della vostra assicurazione sulla vita: incassate 100 €", "stonks": 100, "not_stonks": False, "new_position": False}
        ]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.probability_card)

    def draws_card(self) -> dict:
        # If, during the game, all the cards have been drawn, the deck is reshuffled, and the process restarts from index -1, meaning the first card of the deck.
        if self.index >= 14:
            self.index = -1
            self.shuffle()
        self.index += 1
        return self.probability_card[self.index]