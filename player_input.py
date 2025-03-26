"""
The first game start panel allows players to select the number of participants,
ranging from a minimum of 2 to a maximum of 8 players.

In this screen, players can also enter their names.
Once this initial menu is completed, the game is ready to begin.
The playing order will follow the order of the players in the list.

Written by: Roberto Parodo
"""
import tkinter as tk
from tkinter import ttk

class PlayerInputApp(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menù iniziale")

        self.num_players_label = ttk.Label(self.root, text="Seleziona il numero di giocatori:")
        self.num_players_label.pack(pady=5)

        self.num_players_var = tk.IntVar(value=2)
        self.num_players_combobox = ttk.Combobox(self.root, textvariable=self.num_players_var, state="readonly")
        self.num_players_combobox['values'] = list(range(2, 9))  # Values from 2 to 8
        self.num_players_combobox.bind("<<ComboboxSelected>>", self.update_fields)
        self.num_players_combobox.pack(pady=5)

        self.fields_frame = ttk.Frame(self.root)
        self.fields_frame.pack(pady=10)

        self.validate_button = ttk.Button(self.root, text="Fatto", state="disabled", command=self.validate)
        self.validate_button.pack(pady=10)

        self.player_entries = []
        self.player_names = []
        self.update_fields()
        self.root.mainloop()

    def update_fields(self, event=None):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        self.player_entries.clear()
        num_players = self.num_players_var.get()
        for i in range(num_players):
            label = ttk.Label(self.fields_frame, text=f"Nome giocatore {i + 1}:")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self.fields_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            entry.bind("<KeyRelease>", self.check_fields)
            self.player_entries.append(entry)
        self.check_fields()

    def check_fields(self, event=None):
        if all(entry.get().strip() for entry in self.player_entries):
            self.validate_button.config(state="normal")
        else:
            self.validate_button.config(state="disabled")

    def validate(self):
        self.player_names = [entry.get().strip() for entry in self.player_entries]
        self.root.destroy()