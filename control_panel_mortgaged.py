"""
This script provides a graphical interface for managing the mortgage operations of the cards a player holds.

If a player lacks liquidity, they can choose to mortgage their properties.
In doing so, the bank grants them a certain amount of cash that can be used to continue playing.
However, once a property is mortgaged, the player can no longer collect rent from other players who land on it.

A property can only be mortgaged if it has no existing constructions and is not involved in any pending trade offers.
For this reason, during the selection process, properties with buildings or ongoing offers are not displayed
as mortgageable options.

Written by: Roberto Parodo
"""
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

class PanelControlMortgaged(object):
    def __init__(self, player, update_callback):
        self.player = player
        self.update_callback = update_callback
        self.card_images_no = None
        self.card_remove_mortgage = None
        self.card_mortgage = None
        self.current_label_mortgage = None
        self.current_label_remove_mortgage = None
        self.current_label_card = None
        self.current_card = None
        self.card_images = None
        self.color = None

        self.root = tk.Toplevel()
        self.root.title(f"Pannello di controllo per le ipoteche di {self.player.name}")
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

        self.frame_button_put_mortgage = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.frame_button_put_mortgage.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.button_put_mortgage = tk.Button(self.frame_button_put_mortgage, text="Ipoteca", command=self.put_mortgage)
        self.button_put_mortgage.pack(expand=True)
        self.button_put_mortgage.config(state="disabled")

        self.frame_button_remove_mortgage = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.frame_button_remove_mortgage.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.button_remove_mortgage = tk.Button(self.frame_button_remove_mortgage, text="Rimuovi Ipoteca", command=self.remove_mortgage)
        self.button_remove_mortgage.pack(expand=True)
        self.button_remove_mortgage.config(state="disabled")

        self.frame_button_close = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.frame_button_close.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.button_close = tk.Button(self.frame_button_close, text="Chiudi", command=self.close)
        self.button_close.pack(expand=True)

        self.add_cards()
        self.root.mainloop()

    def put_mortgage(self):
        self.player.mortgaged_cards.append(self.current_card)
        self.player.cards.remove(self.current_card)
        self.player.paid(self.current_card.get_attributes()["mortgage_value"])
        if self.player.check_balance(self.current_card, "mortgage_value"):
            self.button_remove_mortgage.config(state="active")
        else:
            self.button_remove_mortgage.config(state="disabled")
        self.button_put_mortgage.config(state="disabled")
        self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")

    def remove_mortgage(self):
        self.player.mortgaged_cards.remove(self.current_card)
        self.player.cards.append(self.current_card)
        self.player.pay(self.current_card.get_attributes()["mortgage_value"]+(0.1*self.current_card.get_attributes()["mortgage_value"]))
        self.button_remove_mortgage.config(state="disabled")
        self.button_put_mortgage.config(state="active")
        self.balance_label.config(text=f"Saldo attuale: {self.player.balance} €")

    def print_information(self, card):
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

        if hasattr(self, "current_label_mortgage") and self.current_label_mortgage is not None:
            self.current_label_mortgage.destroy()
        self.card_mortgage = card.get_attributes()["mortgage_value"]
        self.current_label_mortgage = tk.Label(self.upper_frame_dx, text=f"Valore ipoteca: {self.card_mortgage} €")
        self.current_label_mortgage.pack(pady=1)

        if hasattr(self, "current_label_remove_mortgage") and self.current_label_remove_mortgage is not None:
            self.current_label_remove_mortgage.destroy()
        self.card_remove_mortgage = card.get_attributes()["mortgage_value"] + (0.1*card.get_attributes()["mortgage_value"])
        self.current_label_remove_mortgage = tk.Label(self.upper_frame_dx, text=f"Costo per togliere l'ipoteca: {self.card_remove_mortgage} €")
        self.current_label_remove_mortgage.pack(pady=1)

        if self.player.search_construction(self.current_card) == -1 and self.current_card.get_attributes()["color"] not in self.color:
            if self.current_card not in self.player.mortgaged_cards:
                self.button_put_mortgage.config(state="active")
            else:
                self.button_put_mortgage.config(state="disabled")
            if self.current_card in self.player.mortgaged_cards:
                if self.player.check_balance(self.current_card, "mortgage_value"):
                    self.button_remove_mortgage.config(state="active")
                else:
                    self.button_remove_mortgage.config(state="disabled")
            else:
                self.button_remove_mortgage.config(state="disabled")
        else:
            messagebox.showinfo("Attenzione",
                                f"Questa proprietà non può essere messa in ipoteca ci sono costruzioni presenti o nei contratti uguali")

    def close(self):
        if self.update_callback:
            self.update_callback(self.player.balance)
        self.root.destroy()

    def add_cards(self):
        max_columns = 7
        row = 0
        col = 0
        self.card_images_no = []
        self.color = []
        for card in self.player.cards:
            if self.player.search_construction(card) != -1:
                self.color.append(self.player.buildings[self.player.search_construction(card)]["card"].get_attributes()["color"])
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