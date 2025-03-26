"""
The GamePanel manages all game windows that will be created throughout the match.

GamePanel Attributes:
    Player: The active player during their turn.

    Banker: The banker responsible for handling purchases, payments, mortgages, and other financial transactions.

    Probability: Object that manages the "Probability" cards.

    Unexpected: Object that manages the "Unexpected" cards.

    Dice: The total rolled by the player's dice.

    Card: The tile where the player lands immediately after rolling the dice.

    Default: A flag indicating whether the player has gone bankrupt.

    Unexpected_station: A flag indicating whether the player has drawn an "Unexpected"
                        card that allows interaction with stations.

    Unexpected_corporation: A flag indicating whether the player has drawn an "Unexpected"
                            card that allows interaction with corporations.


Written by: Roberto Parodo
"""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from control_panel_construction import PanelControlConstruction
from control_panel_mortgaged import PanelControlMortgaged
from control_panel_offert import PanelControlOffer
from panel_show_deck import ShowDeck
from card import Property, Corporation, Station
from players import Player

special_position = [0, 2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38]
list_color = ["light_blue", "pink", "orange", "red", "yellow", "green", "purple", "blue"]

class GamePanel(object):
    def __init__(self, player, banker, probability, unexpected):
        self.player = player
        self.banker = banker
        self.probability = probability
        self.unexpected = unexpected
        self.dice = 0
        self.card = None
        self.default = False
        self.unexpected_station = False
        self.unexpected_corporation = False

        self.root = tk.Tk()
        self.root.title(f"Monopoly, turno giocatore: {self.player.name}")
        self.root.geometry("800x400")

        self.upper_frame = tk.Frame(self.root, height=200, bg="white", relief="ridge", bd=2)
        self.upper_frame.pack(fill="x")

        lower_frame = tk.Frame(self.root, height=200)
        lower_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(lower_frame, width=300, relief="ridge", bd=2)
        left_frame.pack(side="left", fill="both", expand=True)

        left_upper_frame = tk.Frame(left_frame, width=200, relief="ridge", bd=2)
        left_upper_frame.pack(side="top", fill="both", expand=True)

        self.right_frame = tk.Frame(lower_frame, width=300, relief="ridge", bd=2)
        self.right_frame.pack(side="top", fill="both")

        self.right_frame_info = tk.Frame(lower_frame, width=300, relief="ridge", bd=2)
        self.right_frame_info.pack(side="bottom", fill="both")
        self.label_info = ""

        self.cards_purchased_frame = tk.Frame(self.upper_frame, bg="white")
        self.cards_purchased_frame.pack(fill="both", pady=10, expand=True)

        left_upper_frame_info_1 = tk.Frame(left_upper_frame, width=100, relief="ridge", bd=2)
        left_upper_frame_info_1.pack(side="left", fill="both", expand=True)

        left_upper_frame_info_2 = tk.Frame(left_upper_frame, width=100, relief="ridge", bd=2)
        left_upper_frame_info_2.pack(side="right", fill="both", expand=True)

        self.balance_label = tk.Label(left_upper_frame_info_1, text=f"Saldo attuale: {self.player.balance} €")
        self.balance_label.pack(pady=10, expand=True)

        self.button_pay = tk.Button(left_upper_frame_info_1, text="Paga", command=self.pay_effect)
        self.button_pay.pack(pady=5, expand=True)
        self.button_pay.config(state="disabled")

        self.button_buy = tk.Button(left_upper_frame_info_1, text="Compra", command=self.buy_effect)
        self.button_buy.pack(pady=5, expand=True)
        self.button_buy.config(state="disabled")

        self.print_offer()

        self.build = tk.Button(left_upper_frame_info_1, text="Costruisci", command=self.build_effect)
        self.build.pack(pady=5, expand=True)
        self.build.config(state="disabled")
        if self.check_constructions():  # Check if the player can build
            self.build.config(state="active")

        self.button_mortgage = tk.Button(left_upper_frame_info_1, text="Ipoteca", command=self.do_button_mortgage)
        self.button_mortgage.pack(pady=5, expand=True)
        self.button_mortgage.config(state="disabled")
        if len(self.player.cards) or len(self.player.mortgaged_cards):  # Check if the player can put mortgage or delete mortgage
            self.button_mortgage.config(state="active")

        self.button_offer = tk.Button(left_upper_frame_info_1, text="Offerta", command=self.do_offer)
        self.button_offer.pack(pady=5, expand=True)
        self.button_offer.config(state="disabled")

        self.btn_show_deck = tk.Button(left_upper_frame_info_2, text="Mostra carte", command=self.show_deck)
        self.btn_show_deck.pack(pady=5, expand=True)
        self.btn_show_deck.config(state="disabled")
        if len(self.player.cards) > 0 or len(self.player.mortgaged_cards) > 0:
            self.btn_show_deck.config(state="active")

        self.btn_next = tk.Button(left_upper_frame_info_2, text="Fine turno", command=self.next)
        self.btn_next.pack(pady=5, expand=True)
        self.btn_next.config(state="disabled")

        dice_img = Image.open("dice/dice.png")
        dice_img = dice_img.resize((50, 50))
        dice_tk = ImageTk.PhotoImage(dice_img)
        self.button_roll_dice = tk.Button(left_upper_frame_info_2, image=dice_tk, command=self.game_controller)
        self.button_roll_dice.pack(pady=5, expand=True)

        self.print_cards_image()

        self.root.mainloop()

    def print_offer(self):
        counter = 0
        if self.player.offer:  # Check if there are offer
            for index in range(len(self.player.offer)):
                if self.player.offer[counter]["recipient"] == self.player:  # Player has received an offer
                    if self.player.offer[counter]["sender_card"]:
                        if self.player.offer[counter]["money"]: # Case you offer both card and money
                            answer = messagebox.askquestion(f"Hai ricevuto una proposta da parte di {self.player.offer[counter]['sender'].name}",
                                                            f"{self.player.offer[counter]['sender'].name} vorrebbe da te la carta {self.player.offer[counter]['recipient_card'].get_attributes()['name']} in cambio della carta {self.player.offer[counter]['sender_card'].get_attributes()['name']} con {self.player.offer[counter]['money']} €")
                            if answer == "yes":
                                self.banker.swap(self.player.offer[counter]["sender"], self.player, self.player.offer[counter]["recipient_card"], self.player.offer[counter]["sender_card"], self.player.offer[counter]["money"])
                                aus = self.player.offer.copy()
                                removed_element = self.player.offer.pop(counter)
                                aus[counter]["sender"].offer.remove(removed_element)
                                self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                                counter -= 1
                        else: # Case where only the card is offered
                            answer = messagebox.askquestion(
                                f"Hai ricevuto una proposta da parte di {self.player.offer[counter]['sender'].name}",
                                f"{self.player.offer[counter]['sender'].name} vorrebbe da te la carta {self.player.offer[counter]['recipient_card'].get_attributes()['name']} in cambio della carta {self.player.offer[counter]['sender_card'].get_attributes()['name']}")
                            if answer == "yes":
                                self.banker.swap(self.player.offer[counter]["sender"], self.player, self.player.offer[counter]["recipient_card"], self.player.offer[counter]["sender_card"], False)
                                aus = self.player.offer.copy()
                                removed_element = self.player.offer.pop(counter)
                                aus[counter]["sender"].offer.remove(removed_element)
                                self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                                counter -= 1
                    else: # Case where only the money is offered
                        answer = messagebox.askquestion(
                            f"Hai ricevuto una proposta da parte di {self.player.offer[counter]['sender'].name}",
                            f"{self.player.offer[counter]['sender'].name} vorrebbe da te la carta {self.player.offer[counter]['recipient_card'].get_attributes()['name']} in cambio di {self.player.offer[counter]['money']} €")
                        if answer == "yes":
                            self.banker.swap(self.player.offer[counter]["sender"], self.player, self.player.offer[counter]["recipient_card"], False, self.player.offer[counter]["money"])
                            aus = self.player.offer.copy()
                            removed_element = self.player.offer.pop(counter)
                            aus[counter]["sender"].offer.remove(removed_element)
                            self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                            counter -= 1
                    if answer == "no":
                        aus = self.player.offer.copy()
                        removed_element = self.player.offer.pop(counter)
                        aus[counter]["sender"].offer.remove(removed_element)
                        counter -= 1
                counter += 1

    def print_cards_image(self):
        if self.player.cards:
            for card in self.player.cards:
                img_path = card.get_attributes()["path"]
                card_img = Image.open(img_path)
                card_img = card_img.resize((100, 100))
                card_tk = ImageTk.PhotoImage(card_img)
                label_card = tk.Label(self.cards_purchased_frame, image=card_tk, bg="white")
                label_card.image = card_tk
                label_card.pack(side="left", padx=5)
        if self.player.mortgaged_cards:
            for card in self.player.mortgaged_cards:
                img_path = card.get_attributes()["retro"]
                card_img = Image.open(img_path)
                card_img = card_img.resize((100, 100))
                card_tk = ImageTk.PhotoImage(card_img)
                label_card = tk.Label(self.cards_purchased_frame, image=card_tk, bg="white")
                label_card.image = card_tk
                label_card.pack(side="left", padx=5)

    def pay_effect(self):
        if self.banker.property_free(self.card): # If the card is from the bank and the player does not want to buy it
            if self.player.check_balance(self.card, "rent"):
                if self.player.position in [12 ,28]: # If the card is from the bank and is a company
                    self.player.pay(self.dice*self.card.get_attributes()["rent"])
                    messagebox.showinfo("Pagamento",f"Hai effettuato un pagamento a favore della banca di {self.dice*self.card.get_attributes()['rent']} €")
                else:
                    self.player.pay(self.card.get_attributes()["rent"]) # Card is from the bank but is not a company
                    messagebox.showinfo("Pagamento", f"Hai effettuato un pagamento a favore della banca di {self.card.get_attributes()['rent']} €")
                self.button_offer.config(state="active")
            else:
                messagebox.showinfo("Game Over",
                                    f"Sei andato in bancarotta: {self.player.balance - self.card.get_attributes()['rent']}.")
                self.default = True
                self.player.pay(self.card.get_attributes()["rent"])
                self.bankrupt_player()
                self.button_offer.config(state="disabled")
        else:
            owner = self.banker.search_owner(self.card)
            if self.card not in owner.mortgaged_cards: # Check if the paper is not mortgaged
                if self.player.position in [5, 15, 25, 35]: # It is a station
                    rent = owner.all_station()
                    if self.unexpected_station: # You arrived at the station because of the unexpected
                        rent = rent*2
                        self.unexpected_station = False
                    if self.player.balance >= rent: # You can pay
                        self.player.pay(rent)
                        owner.paid(rent)
                        messagebox.showinfo("Pagamento",f"Hai effettuato un pagamento a favore del giocatore: {owner.name} di {rent} €")
                        self.button_offer.config(state="active")
                    else:
                        messagebox.showinfo("Game Over",
                                            f"Sei andato in bancarotta: {self.player.balance - rent} €.")
                        owner.paid(self.player.balance)
                        self.default = True
                        self.bankrupt_player_case(owner)
                        self.button_offer.config(state="disabled")
                elif self.player.position in [12, 28]: # It is a corporation
                    rent = self.dice*owner.all_corporation()
                    if self.unexpected_corporation: # You arrived at the corporation because of the unexpected
                        rent = self.dice*10
                        self.unexpected_corporation = False
                    if self.player.balance >= rent:
                        self.player.pay(rent)
                        owner.paid(rent)
                        messagebox.showinfo("Pagamento", f"Hai effettuato un pagamento a favore del giocatore: {owner.name} di {rent} €")
                        self.button_offer.config(state="active")
                    else:
                        messagebox.showinfo("Game Over",
                                            f"Sei andato in bancarotta: {self.player.balance -  rent} €.")
                        owner.paid(self.player.balance)
                        self.default = True
                        self.bankrupt_player_case(owner)
                        self.button_offer.config(state="disabled")
                else:
                    if owner.all_contract(self.card.get_attributes()["color"]): # If the player owns all the contracts of the same color pays double annuity or with hotel
                        index = owner.search_construction(self.card)
                        cifra = 0
                        if index == -1: # Pays double annuity if it has no construction in the paper
                            cifra = 2 * self.card.get_attributes()["rent"]
                            messagebox.showinfo("Pagamento",
                                                f"Hai effettuato un pagamento con rendita doppia, il giocatore: {owner.name} possiede tutti i contratti di questo colore")
                        else:
                            information = owner.buildings[index]
                            if information["hotel"] == 1: # If the player has hotel
                                cifra = self.card.get_attributes()["hotel"]
                                messagebox.showinfo("Attenzione",
                                                    f"Il giocatore: {owner.name} possiede un Hotel in questa carta")
                            elif information["house"] == 1: # If the player has one house
                                cifra = self.card.get_attributes()["house_1"]
                                messagebox.showinfo("Attenzione",
                                                    f"Il giocatore: {owner.name} possiede una Casa in questa carta")
                            elif information["house"] == 2: # If the player has two house
                                cifra = self.card.get_attributes()["house_2"]
                                messagebox.showinfo("Attenzione",
                                                    f"Il giocatore: {owner.name} possiede due Case in questa carta")
                            elif information["house"] == 3: # If the player has three house
                                cifra = self.card.get_attributes()["house_3"]
                                messagebox.showinfo("Attenzione",
                                                    f"Il giocatore: {owner.name} possiede tre Case in questa carta")
                            elif information["house"] == 4: # If the player has four house
                                cifra = self.card.get_attributes()["house_4"]
                                messagebox.showinfo("Attenzione",
                                                    f"Il giocatore: {owner.name} possiede quattro Case in questa carta")
                        if self.player.balance >= cifra:
                            self.player.pay(cifra)
                            owner.paid(cifra)
                            messagebox.showinfo("Pagamento",f"Hai effettuato un pagamento a favore del giocatore: {owner.name} di {cifra} €")
                            self.button_offer.config(state="active")
                        else:
                            messagebox.showinfo("Game Over",
                                                f"Sei andato in bancarotta: {self.player.balance - cifra} €.")
                            owner.paid(self.player.balance)
                            self.default = True
                            self.bankrupt_player_case(owner)
                            self.button_offer.config(state="disabled")
                    else:
                        if self.player.check_balance(self.card, "rent"):
                            self.player.pay(self.card.get_attributes()["rent"])
                            owner.paid(self.card.get_attributes()["rent"])
                            messagebox.showinfo("Pagamento", f"Hai effettuato un pagamento a favore del giocatore: {owner.name} di {self.card.get_attributes()['rent']} €")
                            self.button_offer.config(state="active")
                        else:
                            messagebox.showinfo("Game Over",
                                                f"Sei andato in bancarotta: {self.player.balance - self.card.get_attributes()['rent']} €.")
                            owner.paid(self.player.balance)
                            self.default = True
                            self.bankrupt_player_case(owner)
                            self.button_offer.config(state="disabled")
            else:
                messagebox.showinfo("Attenzione",
                                        f"La carte è di proprietà del giocatore: {owner.name} ma è in ipoteca quindi non paghi nulla")
        self.button_pay.config(state="disabled")
        self.button_buy.config(state="disabled")
        self.btn_next.config(state="active")
        self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")

    def buy_effect(self):
        self.banker.player_buy(self.player, self.card, "si")
        self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
        self.button_buy.config(state="disabled")
        self.button_pay.config(state="disabled")
        img_path = self.card.get_attributes()["path"]
        card_img = Image.open(img_path)
        card_img = card_img.resize((100, 100))
        card_tk = ImageTk.PhotoImage(card_img)
        label_card = tk.Label(self.cards_purchased_frame, image=card_tk, bg="white")
        label_card.image = card_tk
        label_card.pack(side="left", padx=5)
        if self.check_constructions():
            self.build.config(state="active")
        self.btn_next.config(state="active")
        self.button_mortgage.config(state="active")
        self.btn_show_deck.config(state="active")
        self.button_offer.config(state="active")

    def build_effect(self):
        PanelControlConstruction(self.player, self.banker, self.update_balance_construction)

    def update_balance_construction(self,  new_balance):
        self.player.balance = new_balance
        self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
        self.button_offer.config(state="active")
        if isinstance(self.card, Property) or isinstance(self.card, Corporation) or isinstance(self.card, Station):
            if self.player.check_balance(self.card, "cost") and self.banker.property_free(self.card):
                self.button_buy.config(state="active")

    def check_constructions(self):
        for color in list_color:
            if self.player.all_contract(color):
                return True
        return False

    def do_button_mortgage(self):
        PanelControlMortgaged(self.player, self.update_balance)

    def update_balance(self, new_balance):
        self.player.balance = new_balance
        self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
        if isinstance(self.card, Property) or isinstance(self.card, Corporation) or isinstance(self.card, Station):
            self.button_offer.config(state="active")
            if self.player.check_balance(self.card, "cost") and self.banker.property_free(self.card):
                self.button_buy.config(state="active")
            if self.check_constructions():  # Check if player can build
                self.build.config(state="active")
        for widget in self.cards_purchased_frame.winfo_children():
            widget.destroy()
        self.print_cards_image()

    def do_offer(self):
        PanelControlOffer(self.player, self.banker)

    def show_deck(self):
        ShowDeck(self.player)

    def next(self):
        messagebox.showinfo("Fine turno", "Fine turno")
        self.root.destroy()

    def info_jail(self, dice_repeat):
        if dice_repeat <= 2: # The player did not roll the dice + 3 consecutive times
            if self.player.balance >= 100:  # Check that the player has enough money to make this decision
                answer = messagebox.askquestion("Sei finito in prigione!",
                                                "Scegli: 'Sì' per andare in prigione e saltare 3 turni, oppure 'No' per evitare la prigione pagando 100 €.")
                self.jail(answer)
            elif self.player.balance < 100:
                messagebox.showinfo("Prigione",
                                    "Sei finito in prigione, andrai in prigione e salterai i prossimi 3 turni")
                self.jail("yes")
        else:
            if self.player.balance >= 100:  # Check that the player has enough money to make this decision
                answer = messagebox.askquestion("Sei finito in prigione!",
                                                "Sfortunatamente hai tirato 3 volte consecutive i dadi, scegli: 'Sì' per andare in prigione e saltare 3 turni, oppure 'No' per evitare la prigione pagando 100 €.")
                self.jail(answer)
            elif self.player.balance < 100:
                messagebox.showinfo("Prigione",
                                    "Sfortunatamente hai tirato 3 volte consecutive i dadi e sei finito in prigione, andrai in prigione e salterai i prossimi 3 turni")
                self.jail("yes")

    def jail(self, answer):
        if answer == "yes":
            self.player.position = 10
            self.player.locked = True
            self.player.number_repeat = 0
        else:
            self.player.pay(100)
            self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
            self.player.number_repeat = 0

    def bankrupt_player(self):
        if self.player.cards: # If he has cards
            lost_card = self.player.clear_card()
            self.banker.cards.extend(lost_card)
            self.banker.remove_property(lost_card)
            self.player.buildings.clear()
        if self.player.mortgaged_cards: # If he has mortgaged cards
            lost_card = self.player.clear_card_mortgaged()
            self.banker.cards.extend(lost_card)
            self.banker.remove_property(lost_card)
        if self.player.offer:
            for off in self.player.offer:
                if off["recipient"] == self.player:
                    off["sender"].offer.remove(off)
                elif off["sender"] == self.player:
                    off["recipient"].offer.remove(off)
            self.player.offer.clear()
        self.button_offer.config(state="disabled")
        self.button_mortgage.config(state="disabled")

    def bankrupt_player_case(self, owner: Player): # Case where a player goes bankrupt because of another
        if self.player.cards: # If he has cards
            no_mortgage_cards = self.player.clear_card()
            owner.cards.extend(no_mortgage_cards)
            self.banker.change_property(self.player, owner)
        if self.player.mortgaged_cards: # If he has mortgaged cards
            mortgage_cards = self.player.clear_card_mortgaged()
            owner.mortgaged_cards.extend(mortgage_cards)
            self.banker.change_property(self.player, owner)
        self.player.buildings.clear() # Deletes all constructed properties
        if self.player.offer: # Cancel all offers in which the bankrupt player is involved
            for off in self.player.offer:
                if off["recipient"] == self.player:
                    off["sender"].offer.remove(off)
                elif off["sender"] == self.player:
                    off["recipient"].offer.remove(off)
            self.player.offer.clear()
        self.button_offer.config(state="disabled")
        self.button_mortgage.config(state="disabled")

    def print_image_dice(self, a, b):
        img_path = f"dice/{a}.png"
        card_img = Image.open(img_path)
        card_img = card_img.resize((20, 20))
        card_tk = ImageTk.PhotoImage(card_img)
        label_card = tk.Label(self.right_frame_info, image=card_tk, bg="white")
        label_card.image = card_tk
        label_card.pack(side="right", padx=5)
        img_path = f"dice/{b}.png"
        card_img = Image.open(img_path)
        card_img = card_img.resize((20, 20))
        card_tk = ImageTk.PhotoImage(card_img)
        label_card = tk.Label(self.right_frame_info, image=card_tk, bg="white")
        label_card.image = card_tk
        label_card.pack(side="right", padx=5)

    def print_house_hotel(self, card):
        owner = self.banker.search_owner(card)
        if not self.banker.property_free(self.card) and card.get_attributes()["position"] not in [5, 15, 25, 25, 12, 28] and card not in owner.mortgaged_cards:
            index = owner.search_construction(card)
            if index != -1:
                houses = owner.buildings[index]["house"]
                hotels = owner.buildings[index]["hotel"]
            else:
                houses = 0
                hotels = 0
            img_house = Image.open("icon_h/house.png").resize((15, 15))
            img_hotel = Image.open("icon_h/hotel.png").resize((15, 15))
            house_tk = ImageTk.PhotoImage(img_house)
            hotel_tk = ImageTk.PhotoImage(img_hotel)
            frame_container = tk.Frame(self.right_frame, bg="white")
            frame_container.pack()
            label_house_icon = tk.Label(frame_container, image=house_tk, bg="white")
            label_house_icon.image = house_tk
            label_house_icon.pack(side="left", padx=5)
            label_house_num = tk.Label(frame_container, text=f"{houses}", bg="white", font=("Arial", 8))
            label_house_num.pack(side="left", padx=5)
            label_hotel_icon = tk.Label(frame_container, image=hotel_tk, bg="white")
            label_hotel_icon.image = hotel_tk
            label_hotel_icon.pack(side="left", padx=5)
            label_hotel_num = tk.Label(frame_container, text=f"{hotels}", bg="white", font=("Arial", 8))
            label_hotel_num.pack(side="left", padx=5)

    def find_image_card(self, card):
        if self.banker.property_free(card):
            self.print_image_card(card.get_attributes()["path"])
        else:
            owner = self.banker.search_owner(card)
            if card in owner.cards:
                self.print_image_card(card.get_attributes()["path"])
            elif card in owner.mortgaged_cards:
                self.print_image_card(card.get_attributes()["retro"])

    def probability_effect(self, status):
        if status["stonks"]:
            self.player.paid(status["stonks"])
            self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
        if status["not_stonks"]:
            if status["not_stonks"] == 40:
                house_number, hotel_number = 0, 0
                for building in self.player.buildings:
                    house_number += building["house"]
                    hotel_number += building["hotel"]
                total = (40*house_number) + (115*hotel_number)
                messagebox.showinfo("Attenzione", f"Il totale da pagare è di: {total} €")
                if self.player.balance >= total:
                    self.player.pay(total)
                    self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                    messagebox.showinfo("Attenzione", f"In totale hai pagato {total} €")
                else:
                    self.player.pay(total)
                    self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                    messagebox.showinfo("Game Over",
                                        f"Sei andato in bancarotta: {self.player.balance}.")
                    self.bankrupt_player()
                    self.default = True
            else:
                if self.player.balance >= status["not_stonks"]:
                    self.player.pay(status["not_stonks"])
                    self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                else:
                    self.player.pay(status["not_stonks"])
                    self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                    messagebox.showinfo("Game Over",
                                        f"Sei andato in bancarotta: {self.player.balance}.")
                    self.bankrupt_player()
                    self.default = True
        if status["new_position"]:
            if status["new_position"] == 10: # If he draws card probability of going to prison without passing the go
                self.info_jail(0)
            elif status["new_position"] == -1: # Passes from the start and picks up 200
                self.player.position = 0
        if self.player.balance >= 0:
            self.button_offer.config(state="active")

    def unexpected_effect(self, status):
        if status["new_position"]:
            if status["new_position"] in [13, 24, 25, 39]: # Unexpected cards Parco della vittoria and other
                if self.player.position > status["new_position"]:
                    self.player.paid(200)
                    self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                self.player.position = status["new_position"]
                self.card = self.banker.get_card(self.player.position)
                for widget in self.right_frame.winfo_children():
                    widget.destroy()
                self.player_choice()
            elif status["new_position"] == -3: # Unexpected card to go back
                self.player.position -= 3
                for widget in self.right_frame.winfo_children():
                    widget.destroy()
                if self.player.position == 4:# Property tax
                    self.effect_income_tax()
                elif self.player.position == 33: # Probability
                    self.print_image_card("special_card/probability.png")
                    probability_card = self.probability.draws_card()
                    messagebox.showinfo("Probabilità", f"{probability_card['text']}")
                    self.probability_effect(probability_card)
                    self.button_roll_dice.config(state="disabled")
                    self.button_pay.config(state="disabled")
                    self.button_buy.config(state="disabled")
                    self.btn_next.config(state="active")
                else:
                    self.card = self.banker.get_card(self.player.position)
                    self.player_choice()
            elif status["new_position"] == -1:
                self.player.position = 0
                for widget in self.right_frame.winfo_children():
                    widget.destroy()
                self.print_image_card("special_card/go.png")
            elif status["new_position"] == 30: # If he draws card probability of going to prison without passing the go
                self.info_jail(0)
        if status["not_stonks"]:
            if status["not_stonks"] == 2: # Go as far as the nearest Train Station: if it is vacant you can buy it from the bank; if it is owned by another player, pay the owner double the rent he is normally entitled to
                self.unexpected_station = True
                position_station = [5, 15, 25, 35]
                self.player.position = min((pos for pos in position_station if pos > self.player.position), default=min(position_station))
                self.card = self.banker.get_card(self.player.position)
                for widget in self.right_frame.winfo_children():
                    widget.destroy()
                self.player_choice()
            elif status["not_stonks"] == 10: # Corporation card
                self.unexpected_corporation = True
                position_corporation = [12, 28]
                self.player.position = min((pos for pos in position_corporation if pos > self.player.position), default=min(position_corporation))
                self.card = self.banker.get_card(self.player.position)
                for widget in self.right_frame.winfo_children():
                    widget.destroy()
                self.player_choice()
            elif status["not_stonks"] in [50, 15]:
                if self.player.balance >= status["not_stonks"]:
                    self.player.pay(status["not_stonks"])
                else:
                    self.player.pay(status["not_stonks"])
                    messagebox.showinfo("Game Over",
                                        f"Sei andato in bancarotta: {self.player.balance}.")
                    self.bankrupt_player()
                    self.default = True
                self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
            elif status["not_stonks"] == 25:
                house_number, hotel_number = 0, 0
                for building in self.player.buildings:
                    house_number += building["house"]
                    hotel_number += building["hotel"]
                total = (25*house_number) + (100*hotel_number)
                if self.player.balance >= total:
                    self.player.pay(total)
                    self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                    messagebox.showinfo("Attenzione", f"In totale hai pagato {total} €")
                else:
                    self.player.pay(total)
                    self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                    messagebox.showinfo("Game Over",
                                        f"Sei andato in bancarotta: {self.player.balance}.")
                    self.bankrupt_player()
                    self.default = True

        if status["stonks"]:
            self.player.paid(status["stonks"])
            self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
            self.btn_next.config(state="active")

        if self.player.balance >= 0:
            self.button_offer.config(state="active")
        self.btn_next.config(state="active")

    def player_choice(self):
        self.find_image_card(self.card)
        if not self.player.is_mine(self.card): # if the card is not mine
            self.button_roll_dice.config(state="disabled")
            self.button_pay.config(state="active")
            self.label_info = tk.Label(self.right_frame_info,
                                       text=f"Costo contratto: {self.card.get_attributes()['cost']} €")
            self.label_info.pack(pady=10)
            self.print_house_hotel(self.card)
            if self.player.check_balance(self.card, "cost") and self.banker.property_free(self.card):
                self.button_buy.config(state="active")
        else:  # If card is mine
            self.button_roll_dice.config(state="disabled")
            messagebox.showinfo("Informazioni Carta", "La carta è già tua")
            self.button_offer.config(state="active")
            self.btn_next.config(state="active")

    def effect_income_tax(self):
        self.print_image_card("special_card/200.png")
        messagebox.showinfo("Attenzione", f"Sei finito nella tassa patrimoniale, paghi 200 €")
        if self.player.balance >= 200:
            self.player.pay(200)
            self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
            self.button_offer.config(state="active")
        else:
            self.player.pay(200)
            messagebox.showinfo("Game Over",
                                f"Sei andato in bancarotta: {self.player.balance}.")
            self.bankrupt_player()
            self.default = True
        self.button_roll_dice.config(state="disabled")
        self.button_pay.config(state="disabled")
        self.button_buy.config(state="disabled")
        self.btn_next.config(state="active")

    def print_image_card(self, path):
        card_img = Image.open(path)
        card_img = card_img.resize((200, 200))
        card_tk = ImageTk.PhotoImage(card_img)
        label_card = tk.Label(self.right_frame, image=card_tk)
        label_card.image = card_tk
        label_card.pack(pady=10)

    def game_controller(self):
        last_position = self.player.position
        dice1, dice2 = self.player.pull()
        self.print_image_dice(dice1, dice2)
        self.dice = dice1+dice2
        messagebox.showinfo("Dadi", f"Hai lanciato i dadi: {self.dice}.")
        if self.player.number_repeat > 2:  # This is jail
            self.info_jail(self.player.number_repeat)
            self.root.destroy()
        else:
            if self.player.repeat and self.player.position != 30 and self.player.number_repeat <= 2:
                messagebox.showinfo("Ottimo", f"Concluse le mosse hai diritto a ritirare i dadi. Attento prima di finire in prigione ti rimangono ancora {3-self.player.number_repeat} lanci")
            self.card = self.banker.get_card(self.player.position)
            if last_position + self.dice > 40:
                self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                messagebox.showinfo("Sei passato dal via", f"Ritira 200 €")
            if self.player.position not in special_position: # no jail, unexpected, probability, parking
                self.player_choice()
            else:
                if self.player.position == 4:
                    self.effect_income_tax()
                elif self.player.position == 38:
                    self.print_image_card("special_card/100.png")
                    if self.player.balance >= 100:
                        messagebox.showinfo("Attenzione",f"Sei finito nella tassa di lusso, paghi 100 €")
                        self.player.pay(100)
                        self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                        self.button_offer.config(state="active")
                    else:
                        self.player.pay(100)
                        messagebox.showinfo("Game Over",
                                            f"Sei andato in bancarotta: {self.player.balance}.")
                        self.bankrupt_player()
                        self.default = True
                    self.button_roll_dice.config(state="disabled")
                    self.button_pay.config(state="disabled")
                    self.button_buy.config(state="disabled")
                    self.btn_next.config(state="active")
                elif self.player.position == 30: # This is jail
                    self.print_image_card("special_card/jail.jpg")
                    self.info_jail(0)
                    self.button_roll_dice.config(state="disabled")
                    self.button_pay.config(state="disabled")
                    self.button_buy.config(state="disabled")
                    self.btn_next.config(state="active")
                elif self.player.position in [2, 17, 33]: # this is probability
                    self.print_image_card("special_card/probability.png")
                    probability_card = self.probability.draws_card()
                    messagebox.showinfo("Probabilità", f"{probability_card['text']}")
                    self.probability_effect(probability_card)
                    self.button_roll_dice.config(state="disabled")
                    self.button_pay.config(state="disabled")
                    self.button_buy.config(state="disabled")
                    self.btn_next.config(state="active")
                elif self.player.position in [7, 22, 36]: # this is unexpected
                    self.print_image_card("special_card/imprevisti.png")
                    unexpected_card = self.unexpected.draws_card_u()
                    messagebox.showinfo("Imprevisti", f"{unexpected_card['text']}")
                    self.unexpected_effect(unexpected_card)
                elif self.player.position == 20: # free park
                    self.print_image_card("special_card/free_park.png")
                    self.button_offer.config(state="active")
                    messagebox.showinfo("Parcheggio gratis", f"Sei arrivato nel parcheggio gratis, non dovrai pagare nulla")
                    self.button_roll_dice.config(state="disabled")
                    self.button_pay.config(state="disabled")
                    self.button_buy.config(state="disabled")
                    self.btn_next.config(state="active")
                elif self.player.position == 10: # jail transit
                    self.print_image_card("special_card/transito.jpg")
                    self.button_offer.config(state="active")
                    messagebox.showinfo("Transito prigione", f"Transito")
                    self.button_roll_dice.config(state="disabled")
                    self.button_pay.config(state="disabled")
                    self.button_buy.config(state="disabled")
                    self.btn_next.config(state="active")
                elif self.player.position == 0:
                    self.print_image_card("special_card/go.png")
                    messagebox.showinfo("Sei al Via", f"Ritira 200 €")
                    self.button_offer.config(state="active")
                    self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
                    self.button_roll_dice.config(state="disabled")
                    self.button_pay.config(state="disabled")
                    self.button_buy.config(state="disabled")
                    self.btn_next.config(state="active")