"""
This script creates a graphical interface that allows the user to manage the construction of houses
or hotels on their owned properties.

The panel is accessible via a button in the main screen (panel.py).
A player can open it only if they own all properties of the same color, granting them the right to build.
Specifically, players need to own two properties for blue or brown sets and three for all other colors.

The player selects the property where they want to begin construction.
If they have enough funds, they can proceed with building; otherwise, they can sell houses if already constructed.

Methods in this class:

    get_same_all_contract: Identifies which properties are eligible for construction.

    buy: Allows the player to purchase houses.

    sell: Allows the player to sell houses.

    print_information: Prints details about the selected property.

    add_cards: Displays the properties where construction can take place.

Written by: Roberto Parodo
"""

import tkinter as tk
from PIL import Image, ImageTk

class PanelControlConstruction(object):
    def __init__(self, player, banker, update_callback):
        self.player = player
        self.banker = banker
        self.update_callback = update_callback
        self.list_card = []
        self.card_images = []
        self.current_card = ""
        self.number_house = None
        self.number_hotel = None
        self.house_cost = None
        self.current_label_card = None
        self.current_label_costo = None
        self.current_number_hotel = None
        self.current_number_house = None

        self.get_same_all_contract()
        
        self.root = tk.Toplevel()
        self.root.title(f"Pannello di controllo per le costruzioni di {self.player.name}")
        self.root.geometry("800x400")

        self.upper_frame = tk.Frame(self.root, bg="white", relief="ridge", bd=2)
        self.upper_frame.pack(fill="both", expand=True)

        self.upper_frame_sx = tk.Frame(self.upper_frame, height=300, width=600, bg="white", relief="ridge", bd=2)
        self.upper_frame_sx.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.upper_frame_sx.pack_propagate(False)

        tk.Label(self.upper_frame_sx, text="Contenuto Sinistro", bg="white", fg="white")

        self.upper_frame_dx = tk.Frame(self.upper_frame, height=300, width=200, bg="white", relief="ridge",
                                           bd=2)
        self.upper_frame_dx.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.upper_frame_dx.pack_propagate(False)

        self.label_dx = tk.Label(self.upper_frame_dx, text="Contenuto Destro", bg="white", fg="white")
        self.label_dx.pack(expand=True)

        self.balance_label = tk.Label(self.upper_frame_dx, text=f"Saldo attuale: {self.player.balance} €")
        self.balance_label.pack(pady=1)

        self.lower_frame = tk.Frame(self.root, bg="white", relief="ridge", bd=2, height=100)
        self.lower_frame.pack(fill="x")
        self.lower_frame.pack_propagate(False)

        self.button_frame_buy = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.button_frame_buy.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.button_buy = tk.Button(self.button_frame_buy, text="Compra casa", command=self.buy)
        self.button_buy.pack(expand=True)
        self.button_buy.config(state="disabled")

        self.frame_button_sell = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.frame_button_sell.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.button_sell = tk.Button(self.frame_button_sell, text="Vendi Casa", command=self.sell)
        self.button_sell.pack(expand=True)
        self.button_sell.config(state="disabled")

        self.frame_button_close = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.frame_button_close.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.button_close = tk.Button(self.frame_button_close, text="Chiudi", command=self.close)
        self.button_close.pack(expand=True)

        self.add_cards()

        self.root.mainloop()

    def get_same_all_contract(self):
        color_inside = []
        for card in self.player.cards:
            color = card.get_attributes()["color"]
            if color != "white" and color != "black":
                if self.player.all_contract(color) and color not in color_inside:
                    self.list_card.extend([card for card in self.player.cards if card.get_attributes()["color"] == color])
                    color_inside.append(color)

    def buy(self):
        index = self.player.search_construction(self.current_card)
        if index != -1:
            self.player.buy_house(self.current_card)
            disable_button = self.player.buildings[index]["hotel"] == 1
            self.button_buy.config(state="disabled" if disable_button else "active")
        else:
            self.player.buy_house(self.current_card)
        if not self.player.check_balance(self.current_card, "house_cost"):
            self.button_buy.config(state="disabled")
        self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
        self.current_number_house.config(text=f"Saldo attuale: {self.player.balance} €")
        self.button_sell.config(state="active")
        index = self.player.search_construction(self.current_card)
        construction = self.player.buildings[index]
        self.number_house = construction["house"]
        self.number_hotel = construction["hotel"]
        self.current_number_house.config(text=f"Case costruite: {self.number_house}")
        self.current_number_hotel.config(text=f"Hotel costruiti: {self.number_hotel}")

    def sell(self):
        self.player.sell_house(self.current_card)
        index = self.player.search_construction(self.current_card)
        if index == -1:
            self.button_sell.config(state="disabled")
            self.button_buy.config(state="active")
            self.number_house = 0
            self.number_hotel = 0
            if not self.player.check_balance(self.current_card, "house_cost"):
                self.button_buy.config(state="disabled")
        else:
            self.button_sell.config(state="active")
            self.button_buy.config(state="active")
            construction = self.player.buildings[index]
            self.number_house = construction["house"]
            self.number_hotel = construction["hotel"]
            if not self.player.check_balance(self.current_card, "house_cost"):
                self.button_buy.config(state="disabled")
        self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")
        self.current_number_house.config(text=f"Case costruite: {self.number_house}")
        self.current_number_hotel.config(text=f"Hotel costruiti: {self.number_hotel}")

    def print_information(self, card):
        self.current_card = card
        img_path = card.get_attributes()["path"]
        card_img = Image.open(img_path)
        card_img = card_img.resize((200, 200))
        card_tk = ImageTk.PhotoImage(card_img)
        index = self.player.search_construction(self.current_card)
        if index == -1:
            self.number_house = 0
            self.number_hotel = 0
        else:
            construction = self.player.buildings[index]
            self.number_house = construction["house"]
            self.number_hotel = construction["hotel"]

        if hasattr(self, "current_label_card") and self.current_label_card is not None:
            self.current_label_card.destroy()
        self.current_label_card = tk.Label(self.label_dx, image=card_tk, bg="white")
        self.current_label_card.image = card_tk
        self.current_label_card.pack(side="top", padx=1)

        if hasattr(self, "current_label_costo") and self.current_label_costo is not None:
            self.current_label_costo.destroy()
        self.house_cost = card.get_attributes()["house_cost"]
        self.current_label_costo = tk.Label(self.upper_frame_dx, text=f"Costo casa: {self.house_cost} €")
        self.current_label_costo.pack(pady=1)

        if hasattr(self, "current_number_house") and self.current_number_house is not None:
            self.current_number_house.destroy()
        self.current_number_house = tk.Label(self.upper_frame_dx, text=f"Case costruite: {self.number_house}")
        self.current_number_house.pack(pady=1)

        if hasattr(self, "current_number_hotel") and self.current_number_hotel is not None:
            self.current_number_hotel.destroy()
        self.current_number_hotel = tk.Label(self.upper_frame_dx, text=f"Hotel costruiti: {self.number_hotel}")
        self.current_number_hotel.pack(pady=1)
        self.update_buttons_state()

    def update_buttons_state(self):
        index = self.player.search_construction(self.current_card)
        if index == -1:
            self.button_buy.config(state="active")
            self.button_sell.config(state="disabled")
        else:
            if self.player.buildings[index]["hotel"] == 1:
                self.button_buy.config(state="disabled")
                self.button_sell.config(state="active")
            else:
                self.button_buy.config(state="active")
                self.button_sell.config(state="active")
        if not self.player.check_balance(self.current_card, "house_cost"):
            self.button_buy.config(state="disabled")

    def close(self):
        if self.update_callback:
            self.update_callback(self.player.balance)
        self.root.destroy()

    def add_cards(self):
        max_columns = 7
        row = 0
        col = 0
        self.card_images = []
        for card in self.list_card:
            img_path = card.get_attributes()["path"]
            pil_image = Image.open(img_path).resize((50, 50))
            card_image = ImageTk.PhotoImage(pil_image)
            self.card_images.append(card_image)
            card_button = tk.Button(
                self.upper_frame_sx,
                image=card_image,
                command=lambda c=card: self.print_information(c)
            )
            card_button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col >= max_columns:
                col = 0
                row += 1