"""
This script provides the first graphical interface that the player uses when they want to make an offer
to another player. It displays the cards purchased by other players that are not already involved
in an ongoing offer with another player and do not have any constructions.

The player who wants to make an offer clicks on the image of the card they wish to acquire and then presses
the "Fai un'offerta" button to complete the proposal.

Written by: Roberto Parodo
"""

import tkinter as tk
from PIL import Image, ImageTk
from send_offert import SendOffer

class PanelControlOffer(object):
    def __init__(self, player, banker):
        self.player = player
        self.banker = banker
        self.card_images = None
        self.card_images_no = None
        self.card_cost = None
        self.current_owner = None
        self.current_property_player = None
        self.current_label_card = None
        self.current_label_cost = None
        self.current_card = None

        self.root = tk.Toplevel()
        self.root.title(f"Pannello di controllo per le offerte di {self.player.name}")
        self.root.geometry("800x400")

        self.upper_frame = tk.Frame(self.root, bg="white", relief="ridge", bd=2)
        self.upper_frame.pack(fill="both", expand=True)

        self.upper_frame_sx = tk.Frame(self.upper_frame, height=300, width=600, bg="white", relief="ridge", bd=2)
        self.upper_frame_sx.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.upper_frame_sx.pack_propagate(False)

        tk.Label(self.upper_frame_sx, text="Left content", bg="white", fg="white")

        self.upper_frame_dx = tk.Frame(self.upper_frame, height=300, width=200, bg="white", relief="ridge",
                                           bd=2)
        self.upper_frame_dx.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.upper_frame_dx.pack_propagate(False)

        self.label_dx = tk.Label(self.upper_frame_dx, text="Right content", bg="white", fg="white")
        self.label_dx.pack(expand=True)

        self.balance_label = tk.Label(self.upper_frame_dx, text=f"Il tuo saldo attuale: {self.player.balance} €")
        self.balance_label.pack(pady=1)

        self.lower_frame = tk.Frame(self.root, bg="white", relief="ridge", bd=2, height=100)
        self.lower_frame.pack(fill="x")
        self.lower_frame.pack_propagate(False)

        self.frame_do_offer = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.frame_do_offer.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.btn_do_offer = tk.Button(self.frame_do_offer, text="Fai un offerta", command=self.do_offer)
        self.btn_do_offer.pack(expand=True)
        self.btn_do_offer.config(state="disabled")

        self.lower_button_close = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.lower_button_close.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.button_close = tk.Button(self.lower_button_close, text="Chiudi", command=self.close)
        self.button_close.pack(expand=True)

        self.add_cards()
        self.root.mainloop()

    def do_offer(self):
        self.btn_do_offer.config(state="disabled")
        SendOffer(self.player, self.banker, self.current_card)

    def print_information(self, card):
        self.btn_do_offer.config(state="active")
        self.current_card = card
        img_path = card.get_attributes()["path"]
        card_img = Image.open(img_path)
        card_img = card_img.resize((200, 200))
        card_tk = ImageTk.PhotoImage(card_img)

        if hasattr(self, "current_label_card") and self.current_label_card is not None:
            self.current_label_card.destroy()
        self.current_label_card = tk.Label(self.label_dx, image=card_tk, bg="white")
        self.current_label_card.image = card_tk
        self.current_label_card.pack(side="top", padx=5)

        if hasattr(self, "current_label_cost") and self.current_label_cost is not None:
            self.current_label_cost.destroy()
        self.card_cost = card.get_attributes()["cost"]
        self.current_label_cost = tk.Label(self.upper_frame_dx, text=f"Costo contratto: {self.card_cost} €")
        self.current_label_cost.pack(pady=1)

        if hasattr(self, "current_property_player") and self.current_property_player is not None:
            self.current_property_player.destroy()
        self.current_owner = self.banker.search_owner(card)
        self.current_property_player = tk.Label(self.upper_frame_dx, text=f"Proprietario del contratto: {self.current_owner.name}")

        if self.player.search_offer(self.current_card):
            self.btn_do_offer.config(state="disabled")
        else:
            self.btn_do_offer.config(state="active")

        self.current_property_player.pack(pady=1)

    def close(self):
        self.root.destroy()

    def add_cards(self):
        max_columns = 7
        row = 0
        col = 0
        other_player = []
        for properti in self.banker.properties:
            if properti["player"] != self.player:
                other_player.append(properti["player"])
        other_player = list(set(other_player))
        all_card_no_mortgaged = []
        all_card_mortgaged = []
        color = []
        for p in other_player:
            if p.cards:
                for c in p.cards:
                    if p.search_construction(c) != -1:
                        color.append(p.buildings[p.search_construction(c)]["card"].get_attributes()["color"])
                for c in p.cards:
                    if not p.search_offer(c) and c.get_attributes()["color"] not in color:
                        all_card_no_mortgaged.append(c)
            if p.mortgaged_cards:
                for c in p.mortgaged_cards:
                    if not p.search_offer(c):
                        all_card_mortgaged.append(c)
        self.card_images_no = []
        for card in all_card_no_mortgaged:
            img_path = card.get_attributes()["path"]
            pil_image = Image.open(img_path).resize((50, 50))
            card_image = ImageTk.PhotoImage(pil_image)
            self.card_images_no.append(card_image)
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
        self.card_images = []
        for card in all_card_mortgaged:
            img_path = card.get_attributes()["retro"]
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