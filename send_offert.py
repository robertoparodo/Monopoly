"""
This script handles the construction of the panel used to send trade offers to another player.
Specifically, it builds upon the panel created in the 'control_panel_offert.py' script.

It allows the finalization of the offer, giving the player the option to propose a counteroffer
in exchange for a card they own, a sum of money, or both.

Once the player completes the creation of the offer, the panel automatically closes,
and the trade proposal is sent to the recipient.

Methods in this class:
    add_cards: Displays the available cards the player can offer as a counteroffer.
               Only cards without existing constructions or ongoing, unresolved trades can be selected.

    print_information: Prints the details of the card the player intends to offer.

    do_offer: Sends the trade offer to the recipient.

    check_input: Verifies if a counteroffer includes a monetary component.
                 The player can only offer an amount within their available liquidity,
                 ensuring they do not exceed their financial means.

Written by: Roberto Parodo
"""

import tkinter as tk
from PIL import Image, ImageTk

class SendOffer(object):
    def __init__(self, player, banker, desired_card):
        self.player = player
        self.banker = banker
        self.desired_card = desired_card
        self.current_card = False
        self.card_images = None
        self.card_images_no = None
        self.card_cost = None
        self.current_label_cost = None
        self.current_label_card = None

        self.root = tk.Toplevel()
        self.root.title(f"Spedisci la richiesta di offerta")
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

        self.label_saldo = tk.Label(self.upper_frame_dx, text=f"Il tuo saldo attuale: {self.player.balance} €")
        self.label_saldo.pack(pady=1)

        self.lower_frame = tk.Frame(self.root, bg="white", relief="ridge", bd=2, height=100)
        self.lower_frame.pack(fill="x")
        self.lower_frame.pack_propagate(False)

        self.frame_do_offer = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.frame_do_offer.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.btn_do_offer = tk.Button(self.frame_do_offer, text="Fai un offerta", command=self.do_offer)
        self.btn_do_offer.pack(expand=True)
        self.btn_do_offer.config(state="active")

        self.exchange_value = tk.StringVar()
        validate_cmd = self.root.register(self.check_input)
        entry = tk.Entry(self.frame_do_offer, textvariable=self.exchange_value, validate="key",
                         validatecommand=(validate_cmd, '%P'))
        entry.pack(pady=10)
        label_trade_money = tk.Label(self.frame_do_offer, text="Fai la tua offerta anche in soldi: ")
        label_trade_money.pack(pady=5)

        self.button_frame_close = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.button_frame_close.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.btn_close = tk.Button(self.button_frame_close, text="Chiudi", command=self.close)
        self.btn_close.pack(expand=True)

        self.add_cards()
        self.root.mainloop()

    def check_input(self, value) -> bool:
        if value.isdigit():
            offer = int(value)
            return 0 <= offer <= self.player.balance
        return False

    def do_offer(self) -> None:
        owner = self.banker.search_owner(self.desired_card)
        if self.current_card:
            if self.exchange_value.get():
                self.player.add_offer(self.player, owner, self.current_card, self.desired_card, self.exchange_value.get())
                owner.add_offer(self.player, owner, self.current_card, self.desired_card, self.exchange_value.get())
            else:
                self.player.add_offer(self.player, owner, self.current_card, self.desired_card)
                owner.add_offer(self.player, owner, self.current_card, self.desired_card)
        else:
            self.player.add_offer(self.player, owner, False, self.desired_card, self.exchange_value.get())
            owner.add_offer(self.player, owner, False, self.desired_card, self.exchange_value.get())
        self.btn_do_offer.config(state="disabled")
        self.root.destroy()

    def print_information(self, card) -> None:
        self.current_card = card
        if card in self.player.cards:
            img_path = card.get_attributes()["path"]
        else:
            img_path = card.get_attributes()["retro"]
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

    def close(self) -> None:
        self.root.destroy()

    def add_cards(self) -> None:
        max_columns = 7
        row = 0
        col = 0
        self.card_images_no = []
        color = []
        for card in self.player.cards:
            if self.player.search_construction(card) != -1:
                color.append(self.player.buildings[self.player.search_construction(card)]["card"].get_attributes()["color"])
        for card in self.player.cards:
            if not self.player.search_offer(card) and card.get_attributes()["color"] not in color:
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
        for card in self.player.mortgaged_cards:
            if not self.player.search_offer(card):
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