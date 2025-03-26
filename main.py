"""
Main script for the Monopoly game.
This script manages the flow of the game, including player turns, handling skipped turns, and removing bankrupt players.
To start the game, execute the main function in this script.
Main features:
 - Dynamic management of player turns.
 - Handling players who need to skip their turn (e.g., due to cards or penalties).
 - Automatic removal of players who go bankrupt.

Written by: Roberto Parodo
"""

from player_input import PlayerInputApp
from players import Player, Banker
from panel import GamePanel
from unexpected_probability import Probability, Unexpected

if __name__ == '__main__':
    app = PlayerInputApp()
    player_list = [Player(p.capitalize()) for p in app.player_names]
    banker = Banker()
    probability = Probability()
    unexpected = Unexpected()
    default_player = []
    counter_turn = 1
    while True:
        print("Turno: ", counter_turn)
        if len(player_list) == 1: # if only one player remains, the game ends
            print("La partita è stata vinta dal giocatore: ", player_list[0].name)
            break
        for p in player_list:
            repeat_number = 1
            if not p.locked: # checks that the player has not gone to prison
                desk = GamePanel(p, banker, probability, unexpected)
                if desk.default:
                    default_player.append(p)
                    p.repeat = False
                while p.repeat and not p.locked: # if the player makes the same score in both dice entitled to withdraw them
                    p.repeat = False
                    desk = GamePanel(p, banker, probability, unexpected)
                    if desk.default:
                        default_player.append(p)
                        p.repeat = False
                    repeat_number += 1
            else:
                p.counter_lock += 1
                if p.counter_lock == 3:
                    p.locked = False
                    p.counter_lock = 0
        # To remove the default player from the list
        if len(default_player) > 0:
            if len(player_list) == len(default_player):
                print("La partita è finità in parità, tutti i giocatori sono andanti in bancarotta nello stesso turno")
                break
            else:
                for p_d in default_player:
                    player_list.remove(p_d)
                default_player.clear()
        counter_turn += 1