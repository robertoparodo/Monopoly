"""
A small panel that opens, allowing the player to view all the cards they have available.

Written by: Roberto Parodo
"""

import tkinter as tk
from PIL import Image, ImageTk

class ShowDeck(object):
    def __init__(self, player):
        self.player = player
        self.card_images = None
        self.card_images_no = None

        self.root = tk.Toplevel()
        self.root.title(f"Le carte che hai acquistato")
        self.root.geometry("1000x500")

        self.upper_frame = tk.Frame(self.root, bg="white", relief="ridge", bd=2)
        self.upper_frame.pack(fill="both", expand=True)

        self.lower_frame = tk.Frame(self.root, bg="white", relief="ridge", bd=2, height=100)
        self.lower_frame.pack(fill="x")
        self.lower_frame.pack_propagate(False)

        self.frame_button_close = tk.Frame(self.lower_frame, bg="white", relief="ridge", bd=2)
        self.frame_button_close.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.button_close = tk.Button(self.frame_button_close, text="Chiudi", command=self.close)
        self.button_close.pack(expand=True)

        self.add_cards()
        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def add_cards(self):
        max_columns = 9
        row = 0
        col = 0
        self.card_images_no = []
        for card in self.player.cards:
            if not self.player.search_offer(card):
                img_path = card.get_attributes()["path"]
                pil_image = Image.open(img_path).resize((90, 90))
                card_image = ImageTk.PhotoImage(pil_image)
                self.card_images_no.append(card_image)
                card_button = tk.Label(
                    self.upper_frame,
                    image=card_image,
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
                pil_image = Image.open(img_path).resize((90, 90))
                card_image = ImageTk.PhotoImage(pil_image)
                self.card_images.append(card_image)
                card_button = tk.Label(
                    self.upper_frame,
                    image=card_image,
                )
                card_button.grid(row=row, column=col, padx=5, pady=5)
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1