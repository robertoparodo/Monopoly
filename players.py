"""
This script defines the Player and Banker objects, the main characters in the game of Monopoly.

Player Attributes:
    Name: The name of the player.

    Balance: The player's available funds, which start at 1,500 coins according to the official rules.

    Position: The player's location on the board (all players start at "GO", position 0).

    Buildings: A list of dictionaries containing information about the player's constructions, including:
        The property card associated with the buildings.
        The number of houses built.
        The number of hotels built.

    Cards: A list of property cards the player has acquired during the game.

    Mortgaged_cards: A list of property cards the player has mortgaged.
                     Cards in this list are no longer in the Cards list and vice versa.

    Locked: A boolean flag indicating whether the player is in jail (True if in jail, False otherwise).

    Repeat: A boolean flag indicating whether the player can roll the dice again, which occurs when rolling doubles.

    Offer: A list of dictionaries containing trade offers received by the player. Each offer includes:
        The recipient.
        The sender.
        The properties involved in the trade.
        Any additional monetary compensation.

    Number_repeat: A counter tracking how many times the player has rolled again in a turn. If this reaches 3, the player is sent to jail.

    Counter_lock: A counter tracking how many turns the player has skipped while in jail. If this reaches 4, the player is released back into the game.

Banker Attributes:
    Total_capital: The total amount of money held by the bank.

    Cards: A list of property cards owned by the bank, meaning they have not yet been purchased by any player.
           Once a player buys a card, it is removed from this list.

    Properties: A list of dictionaries that records which player owns each property card.
                This helps identify the owner of a given property.

Written by: Roberto Parodo
"""

import random, pandas as pd
from card import Property, Station, Corporation

class Player(object):
    def __init__(self, name):
        self.name = name
        self.balance = 1500
        self.position = 0
        self.buildings = []
        self.cards = []
        self.mortgaged_cards = []
        self.locked = False
        self.repeat = False
        self.offer = []
        self.number_repeat = 0
        self.counter_lock = 0

    def pull(self):
        """
        This method allows the player to roll the dice. If both dice show the same number (doubles):
            The number_repeat counter is incremented.
            The repeat flag is set to True.
            If number_repeat reaches 3, the player is sent to jail.
        If the player does not roll doubles:
            number_repeat is reset to 0.
            The repeat flag set to False.
        After these operations, the set_position method to update the player's new position on the board.
        Finally, the rolled dice values returned.
        :return: dice_a: int, dice_b: int
        """
        dice_a = random.randint(1, 6)
        dice_b = random.randint(1, 6)
        if dice_a == dice_b:
            self.repeat = True
            self.number_repeat += 1
        else:
            self.repeat = False
            self.number_repeat = 0
        self.set_position(dice_a + dice_b)
        return dice_a, dice_b

    def all_contract(self, color) -> bool:
        """
        This method checks whether a player owns all the property cards of a specific color group.
        To verify this, the method checks if the player has all the required cards of the given color:
            For brown and blue properties, the player must own 2 cards.
            For all other colors, the player must own 3 cards.
        :param: color (str): The color of the property set to check.
        :return: True if the player owns all the properties of the specified color.
                 False if the player is missing any properties from the set.
        """
        list_color = ["light_blue", "pink", "orange", "red", "yellow", "green"]
        number = 0
        for card in self.cards:
            if card.get_attributes()["color"] == color:
                number += 1
        if color == "purple" and number == 2:
            return True
        elif color == "blue" and number == 2:
            return True
        elif color in list_color and number == 3:
            return True
        return False

    def add_offer(self, sender, recipient, sender_card=False, recipient_card=False, money=False):
        """
        Adds an exchange proposal
        """
        self.offer.append({
            "sender": sender,
            "recipient": recipient,
            "sender_card": sender_card,
            "recipient_card": recipient_card,
            "money": money
        })

    def all_corporation(self) -> int | None:
        """
        This method checks whether the player owns utility properties and returns a multiplier to calculate the rent
        for opponents landing on them.
        Utilities are assigned the color black (a neutral color that does not conflict with standard property colors).
        The method verifies whether the player owns both utility properties.
        The rent calculation depends on the number of utilities owned:
            1 utility: Rent is 4× the total value rolled on the dice.
            2 utilities: Rent is 10× the total value rolled on the dice.
        :return:
            4 if the player owns one utility.
            10 if the player owns both utilities.
        """
        number = 0
        for card in self.cards:
            if card.get_attributes()["color"] == "black":
                number += 1
        if number == 1:
            return 4
        elif number == 2:
            return 10

    def all_station(self) -> int | None:
        """
        This method searches the player's deck for owned stations.
        Stations are identified using the color white (a neutral color that does not conflict with standard property colors).
        The rent value depends on the number of stations the player owns:
            1 station: Rent = 25
            2 stations: Rent = 50
            3 stations: Rent = 100
            4 stations (all owned): Rent = 200
        :return: The rent amount that must be paid to the station owner.
        """
        number = 0
        for card in self.cards:
            if card.get_attributes()["color"] == "white":
                number += 1
        if number == 1:
            return 25
        elif number == 2:
            return 50
        elif number == 3:
            return 100
        elif number == 4:
            return 200

    def is_mine(self,  card) -> bool:
        """
        This method verifies whether a specific card belongs to the player.
        It also checks if the card is in the mortgaged deck.
        :param: card (object): The card to search for.
        :return:
            True if the player owns the card.
            False if the player does not own it.
        """
        return card in self.cards or card in self.mortgaged_cards

    def paid(self, money_amount):
        """
        This method increases the player's balance by adding a specified amount of money.
        :param: money_amount (int): The amount of money to add to the player's balance.
        """
        self.balance += money_amount

    def pay(self, cost):
        """
        This method deducts a specified amount from the player's balance.
        :param: cost (int): The amount the player must pay.
        """
        self.balance -= cost

    def add_card(self, card):
        """
        This method adds a purchased or received card to the player's deck.
        :param: card (object): The card that the player has bought or acquired.
        """
        self.cards.append(card)

    def add_mortgaged_card(self, card):
        """
        This method adds a card that the player already owns to the mortgaged deck.
        :param: card (object): The card that the player wants to mortgage.
        """
        self.mortgaged_cards.append(card)

    def check_balance(self, card, what) -> bool:
        """
        This method checks if the player has enough balance to perform certain operations, such as:
        Removing the mortgage from a previously mortgaged card.
        Paying rent to the bank or another player if they own the property the player landed on.
        :param:
            card (object): The card the player landed on.
            what (str): A string that defines the type of operation, such as "simple rent" or "rent with houses or hotel."
        :return:
            True if the player can afford the operation (removing the mortgage or paying rent).
            False if the player cannot afford it.
        """
        if what == "mortgage_value":
            # This method checks if the player has enough balance to remove the mortgage from a card.
            # To do so, the player must pay the mortgage value plus a 10% surcharge.
            return self.balance >= card.get_attributes()[what]+(0.1*card.get_attributes()[what])
        else:
            return self.balance >= card.get_attributes()[what]

    def clear_card(self):
        """
        When a player goes bankrupt, their deck of non-mortgaged cards is cleared.
        :return: The bankrupt player's cards are transferred to the player who caused their bankruptcy or to the bank.
        """
        aus_cards = self.cards.copy()
        self.cards.clear()
        return aus_cards

    def clear_card_mortgaged(self):
        """
        When a player goes bankrupt, their mortgaged deck cards is cleared.
        :return: The bankrupt player's cards are transferred to the player who caused their bankruptcy or to the bank.
        """
        aus_cards = self.mortgaged_cards.copy()
        self.mortgaged_cards.clear()
        return aus_cards

    def set_position(self, new_position):
        """
        Method to move the player within the game board.
        If the new position is 40 (the "Go" space), the position is set to 0, and the player receives 200 coins,
        as they earn 200 each time they pass "Go."
        If the new position exceeds 40, the player moves to "Go" and receives the remaining steps from the dice roll,
        along with the 200 coins.
        Otherwise, the player moves forward by the total rolled on the dice.
        :param new_position: The total result of the dice roll.
        """
        if (self.position+new_position) == 40:
            self.position = 0
            self.balance += 200
        elif (self.position+new_position) > 40:
            aus = (self.position+new_position) - 40
            self.position = aus
            self.balance += 200
        else:
            self.position += new_position

    def buy_house(self, card):
        """
        Method that allows the player to build houses or hotels.
        First, it checks whether there are already constructions on the property contract.
        If index is -1, there are no existing buildings; otherwise, there are.
        If no buildings are present, a dictionary is added to the buildings list containing information such as:
            The property card where buildings are placed
            The number of houses built
            The number of hotels built
        If constructions already exist and the maximum number of houses allowed for the property has not been reached,
        an additional house can be built; otherwise, no further houses can be added.
        The player must pay the cost specified in the contract for each house built.
        :param card: The property contract on which the player wants to build.
        """
        index = self.search_construction(card)
        if index < 0:
            self.buildings.append({"card": card, "house":1, "hotel":0})
            self.pay(card.get_attributes()["house_cost"])
        else:
            if self.buildings[index]["hotel"] != 1:
                self.pay(card.get_attributes()["house_cost"])
            self.add_house(index)

    def sell_house(self, card):
        """
        Method to sell buildings on a property contract.
        Sold houses earn the property owner half of their original purchase price.
        If there is a hotel on the property, it is removed and replaced with four houses.
        If only houses are present, they are removed one by one each time the player sells a building
        until there are none left, leaving the property without any constructions.
        :param card: The property contract on which the player wants to sell houses or hotel.
        """
        self.paid((card.get_attributes()["house_cost"] * 50) / 100)
        position = self.search_construction(card)
        if self.buildings[position]["hotel"] == 1:
            self.buildings[position]["hotel"] = 0
            self.buildings[position]["house"] = 4
        else:
            if self.buildings[position]["house"] == 1:
                self.buildings[position]["house"] = 0
                self.buildings.pop(position)
            else:
                self.buildings[position]["house"] -= 1

    def search_construction(self, card) -> int:
        """
        Method to search for buildings within a property contract.
        :param card: The property card on which to check for existing buildings.
        :return: The position of the property within the buildings list, or -1 if no buildings are present.
        """
        position = 0
        for buildings in self.buildings:
            if buildings["card"] == card:
                return position
            position += 1
        return -1

    def add_house(self, position: int):
        """
        Method to add a building to a property contract.
        If a hotel is already present on the property, the maximum building limit has been reached.
        If there are already four houses, the house count is set to -1, and one hotel is added.
        If there are fewer than four houses, the house count is incremented.
        :param position: The position of the contract on which the player wants to build.
        """
        if self.buildings[position]['hotel'] != 1:
            if self.buildings[position]['house'] == 4:
                self.buildings[position]['hotel'] += 1
                self.buildings[position]['house'] = -1
            self.buildings[position]['house'] += 1

    def search_offer(self, card) -> bool:
        """
        Method to check for active offers on a specific card.
        :param card: The card being checked for ongoing trade offers.
        :return: True if there are trade offers for the player or if the player has made offers. False otherwise.
        """
        for offer in self.offer:
            if offer["sender_card"] == card or offer["recipient_card"] == card:
                return True
        return False


class Banker(object):
    def __init__(self):
        self.total_capital = 1000000
        self.cards = []
        self.properties = []
        self.start_deck()

    def get_card(self, position):
        """
        Method to return the card on which the player has landed.
        :param position: The board position where the player has landed.
        :return: the card corresponding to the player's current position.
        """
        for card in self.cards:
            if position == card.position:
                return card
        for player_properties in self.properties:
            if player_properties["card"].get_attributes()["position"] == position:
                return player_properties["card"]

    def search_owner(self, card) -> Player | None:
        """
        Method to retrieve the owner of a card.
        :param card: The card whose owner is being determined.
        :return: The owner of the card, represented as a Player object.
        """
        for pl in self.properties:
            if card == pl["card"]:
                return pl["player"]

    def player_buy(self, player: Player, card, answer) -> bool | None:
        if player.balance >= card.get_attributes()["cost"] and self.property_free(card) and answer.lower()=="si":
            player.pay(card.get_attributes()["cost"])
            player.add_card(card)
            self.properties.append({"player": player, "card": card})
            self.cards.remove(card)
            return True
        elif card in self.cards:
            player.pay(card.get_attributes()["rent"])
            return False
        else:
            for player_properties in self.properties:
                if player_properties["card"].name == card.name:
                    owner = player_properties["player"]
                    player.pay(card.get_attributes()["rent"])
                    owner.paid(card.get_attributes()["rent"])
                    return False

    def property_free(self, card) -> bool:
        """
        Checks if the card does not belong to another player.
        :param card: The card on which the player has landed.
        :return: True if the card belongs to the bank. False otherwise.
        """
        return card in self.cards

    def remove_property(self, deck):
        self.properties = [prop for prop in self.properties if prop["card"] not in deck]

    def change_property(self, bankrupt_player, new_owner):
        """
        Method to transfer properties when a player goes bankrupt due to another player. The player responsible for the bankruptcy has the right to receive the bankrupt player's cards.
        :param:
            bankrupt_player: The player who has gone bankrupt.
            new_owner: The player who is entitled to receive the bankrupt player's cards.
        """
        for player_properties in self.properties:
            if player_properties["player"] == bankrupt_player:
                player_properties["player"] = new_owner

    def swap(self, new_owner: Player, old_owner: Player, card1, card2=False, money=False):
        """
        Method used when the counterpart of the offer accepts the trade proposal.
        It updates the properties of the players involved and modifies their decks accordingly.
        :param:
            new_owner: The player who accepted the offer.
            old_owner: The player who proposed the trade.
            card1: The card that goes to the player who accepted the trade.
            card2: The card that goes to the player who proposed the trade, if applicable.
            money: The amount of money the player who accepted the offer will receive, if applicable.
        The trade proposal must include at least one card, at least the money, or both.
        """
        for pl in self.properties:
            if pl["player"] == old_owner and pl["card"] == card1:
                pl["player"] = new_owner
        if card1 in old_owner.cards:
            old_owner.cards.remove(card1)
            new_owner.add_card(card1)
        elif card1 in old_owner.mortgaged_cards:
            old_owner.mortgaged_cards.remove(card1)
            new_owner.add_mortgaged_card(card1)
        if card2:
            for pl in self.properties:
                if pl["player"] == new_owner and pl["card"] == card2:
                    pl["player"] = old_owner
            if card2 in new_owner.cards:
                new_owner.cards.remove(card2)
                old_owner.add_card(card2)
            elif card2 in new_owner.mortgaged_cards:
                new_owner.mortgaged_cards.remove(card2)
                old_owner.add_mortgaged_card(card2)
        if money:
            new_owner.pay(int(money))
            old_owner.paid(int(money))

    def start_deck(self):
        """
        Method of initializing all cards that players can purchase (Contract, Station, Corporation)
        """
        contract = pd.read_csv("csv/contract.csv")
        station = pd.read_csv("csv/station.csv")
        corporation = pd.read_csv("csv/corporation.csv")
        contract = contract.to_dict(orient="records")
        station = station.to_dict(orient="records")
        corporation = corporation.to_dict(orient="records")
        for i in contract:
            self.cards.append(Property(
                i["name"],
                i["rent"],
                i["house_1"],
                i["house_2"],
                i["house_3"],
                i["house_4"],
                i["hotel"],
                i["house_cost"],
                i["mortgage_value"],
                i["color"],
                i["position"],
                i["cost"],
                i["path"],
                i["retro"]
            ))
        for i in station:
            self.cards.append(Station(
                i["name"],
                i["rent"],
                i["station_2"],
                i["station_3"],
                i["station_4"],
                i["mortgage_value"],
                i["position"],
                i["cost"],
                i["path"],
                i["color"],
                i["retro"]
            ))
        for i in corporation:
            self.cards.append(Corporation(
                i["name"],
                i["rent"],
                i["corporation_2"],
                i["mortgage_value"],
                i["position"],
                i["cost"],
                i["path"],
                i["color"],
                i["retro"]
            ))