# Poker Game v1.0
"""
@author: Dan_Evan (ElofHew)
@version: 1.0_demo
@date: 2025-01-04
@license: MIT
"""

import os
import time
import sys
import json
import random

with open('config.json', 'r') as f:
    config = json.load(f)
    player = config['player']
    timeout = config['timeout']
    best_score = config['best_score']

cards = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2'] * 4 + ['joker', 'JOKER']
random.shuffle(cards)
player1 = cards[0:17]
player2 = cards[17:34]
player3 = cards[34:51]
bottom_cards = cards[51:54]

card_order = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'joker', 'JOKER']
card_rank = {card: i for i, card in enumerate(card_order)}

def choose_first_person():
    print("=== Choosing the Landlord... ===")
    time.sleep(0.5)
    landlord = random.randint(1, 3)
    if landlord == 1:
        print("Player 1 (You) is the landlord.")
        print(f"Bottom Cards: \n{bottom_cards}")
        player1.extend(bottom_cards)
        print(f"Your Cards: \n{player1}")
    elif landlord == 2:
        print("Player 2 (Bot) is the landlord.")
        player2.extend(bottom_cards)
    else:
        print("Player 3 (Bot) is the landlord.")
        player3.extend(bottom_cards)
    return landlord

def game_menu(landlord):
    print("=== Game Start ===")
    print("Here have some Tips: \n"
          "1. enter the number of your card to hand out.\n"
          "2. enter pass to pass this round.\n"
          "3. enter exit to end the game.\n"
          "Good luck to you!")
    print("(The game will start in 5 seconds.)")
    time.sleep(5)

def play_round(current_player, last_played=[]):
    print(f"Current Player: Player {current_player}")
    if current_player == 1:
        print("Your Cards:", player1)
        while True:
            choice = input("Your move: ")
            if choice == 'exit':
                sys.exit()
            elif choice == 'pass':
                print("You passed.")
                return last_played
            else:
                choices = choice.split(',')
                choices = [player1.pop(int(c) - 1) for c in choices]
                if is_valid_play(choices, last_played):
                    print("You played:", choices)
                    return choices
                else:
                    print("Invalid play, try again.")
    else:
        bot_play = bot_decision(player2 if current_player == 2 else player3, last_played)
        if bot_play:
            print(f"Bot {current_player} played:", bot_play)
        else:
            print(f"Bot {current_player} passed.")
        return bot_play

def is_valid_play(play, last_played):
    # 简单判断是否为空，以后加入更多的规则
    if not last_played:
        return True
    return False

def bot_decision(player_cards, last_played):
    # 简单随机出牌，以后加入更复杂的策略
    if last_played:
        return []
    else:
        return [player_cards.pop(random.randint(0, len(player_cards) - 1))]

def game_start():
    print("Loading...")
    time.sleep(0.5)
    print("Timeout: ", timeout, "seconds")
    print("Do you want to change these configurations? (y/n)")
    while True:
        try:
            chs2 = input("> ")
            if chs2 == 'y':
                settings()
                break
            elif chs2 == 'n':
                print("No configuration had changed.")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        except:
            print("Invalid input. Please enter 'y' or 'n'.")
    print("Loading...")
    time.sleep(0.5)
    print("Tips: joker is smaller than JOKER.")
    landlord = choose_first_person()
    game_menu(landlord)
    # 轮流出牌，这里简化为3轮，以后扩展为无限轮
    for _ in range(3):
        for player in [1, 2, 3]:
            play_round(player)
    sys.exit()

def settings():
    while True:
        try:
            print("=================================")
            print("       Poker Game Settings       ")
            print("1. Player Name")
            print("2. Game Timeout")
            print("3. Back to Main Menu")
            print("=================================")
            settings_chs = input("> ")
            if settings_chs == '1':
                while True:
                    try:
                        print("Last Player Name: ", player)
                        player = input("Enter your new name: ")
                        with open('config.json', 'w') as f:
                            config['player'] = player
                            json.dump(config, f)
                        print("Player name changed successfully!")
                        print("New Player Name: ", player)
                        break
                    except:
                        print("Invalid input. Please enter a valid name.")
            elif settings_chs == '2':
                while True:
                    try:
                        while True:
                            try:
                                timeout = int(input("Enter a new timeout (in 3s~60s): "))
                                if timeout < 3 or timeout > 60:
                                    print("Invalid input. Please enter a number from 3 to 60.")
                                else:
                                    with open('config.json', 'w') as f:
                                        config['timeout'] = timeout
                                        json.dump(config, f)
                                    break
                            except:
                                print("Invalid input. Please enter a number from 3 to 60.")
                        print("Timeout changed successfully!")
                        print("New Timeout: ", timeout, "seconds")
                        break
                    except:
                        print("Invalid input. Please enter a number from 3 to 60.")
            elif settings_chs == '3':
                return menu()
            else:
                print("Invalid input. Please enter a number from 1 to 4.")
        except:
            print("Invalid input. Please enter a number from 1 to 4.")

def about():
    print("=============================")
    print("       About This Game       ")
    print("=============================")
    print("Author: Dan_Evan (ElofHew)\n"
            "Version: 1.0\n"
            "Date: 2025-01-04\n"
            "Description: A simple poker game. A player vs computer.\n"
            "If you can, please give me a star on GitHub: https://github.com/ElofHew/PokerGame\n"
            "And subscribe my bilibili channel: https://space.bilibili.com/642688364\n"
            "Thanks for playing!")
    return menu()

def menu():
    while True:
        try:
            print("=================================")
            print("      Welcome to Poker Game      ")
            print("1. Start Game")
            print("2. Settings")
            print("3. About")
            print("4. Exit")
            print("=================================")
            menu_chs = input("> ")
            if menu_chs == '1':
                return game_start()
            elif menu_chs == '2':
                return settings()
            elif menu_chs == '3':
                return about()
            elif menu_chs == '4':
                print("Do you want to exit the game? (y/n)")
                while True:
                    try:
                        chs3 = input("> ")
                        if chs3 == 'y':
                            sys.exit()
                        elif chs3 == 'n':
                            break
                        else:
                            print("Invalid input. Please enter 'y' or 'n'.")
                    except ValueError:
                        print("Invalid input. Please enter 'y' or 'n'.")
            else:
                print("Invalid input. Please enter a number from 1 to 4.")
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 4.")

print("==============================")
print("          Poker Game          ")
print("==============================")
print("Your best_score is: ", best_score)
print("Player Name: ", player)
print("Would you want to change your name? (y/n)")
while True:
    try:
        chs1 = input("> ")
        if chs1 == 'y':
            player = input("Enter your new name: ")
            with open('config.json', 'w') as f:
                config['player'] = player
                json.dump(config, f)
            print("Name changed successfully!")
            time.sleep(0.5)
            print("New Player Name: ", player)
            break
        elif chs1 == 'n':
            print("Name not changed.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
    except:
        print("Invalid input. Please enter 'y' or 'n'.")
menu()
