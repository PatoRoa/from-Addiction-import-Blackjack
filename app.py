import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import random


#function to switch screens
def show_frame(frame):
    frame.tkraise() #bring the frame to the front


def goto_game():
    show_frame(game_screen)
    start_round()


# Keeps garbage collection from deleting the actual photos
player_card_images = []
dealer_card_images = []

# Store cards that the player and dealer have
player_hand = []
dealer_hand = []

wins = 0
losses = 0

# Setting up the suits and cards
suits = ["club", "diamond", "heart", "spade"]
ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]

# Create full deck of 52 cards
deck = [(s, r) for s in suits for r in ranks]


############################## CARD FUNCTIONS ##############################
# Draw card function
def draw_card():
    return random.choice(deck)


def card_to_filename(card):
    suit, rank = card
    return f"cards/{suit}_{rank}.png"


def show_card(card, frame, image_list):
    filename = card_to_filename(card)
    img = tk.PhotoImage(file=filename).subsample(3)

    image_list.append(img)  # prevent garbage collection

    label = tk.Label(frame, image=img, bg="green")
    label.pack(side="left")


############################ GAME FUNCTIONS ####################################
def start_round():
    player_hand.clear()
    dealer_hand.clear()
    player_card_images.clear()
    dealer_card_images.clear()

    # Clear card frames
    for widget in player_cards_frame.winfo_children():
        widget.destroy()

    for widget in dealer_cards_frame.winfo_children():
        widget.destroy()

    # Deal cards to the player
    card1 = draw_card()
    card2 = draw_card()
    player_hand.extend([card1, card2])
    show_card(card1, player_cards_frame, player_card_images)
    show_card(card2, player_cards_frame, player_card_images)

    # Deal one card to dealer (second card hidden later)
    dealer_card1 = draw_card()
    dealer_card2 = draw_card()
    dealer_hand.extend([dealer_card1, dealer_card2])
    # dealer_hand.append(dealer_card)

    # Show first card face up
    show_card(dealer_card1, dealer_cards_frame, dealer_card_images)

    # Show back of second card
    hidden_Label = tk.Label(dealer_cards_frame, image=card_back, bg='green')
    hidden_Label.pack(side="left")

    global dealer_hidden_label
    dealer_hidden_label = hidden_Label

    hit_button.config(state="normal")
    stand_button.config(state="normal")


def player_hit():
    card = draw_card()
    player_hand.append(card)
    show_card(card, player_cards_frame, player_card_images)

    # Check for bust
    if calculate_hand_value(player_hand) > 21:
        messagebox.showinfo("Bust", "You busted! Dealer wins.")
        end_round(player_lost=True)


############################# GAME LOGIC ####################################
def calculate_hand_value(hand):
    value = 0
    aces = 0

    for card in hand:
        suit, rank = card

        if rank in ["jack", "queen", "king"]:
            value += 10
        elif rank == "1":
            aces += 1
            value += 11   # temporarily treat all aces as 11
        else:
            value += int(rank)

    # If value is over 21, convert some aces from 11 → 1
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value


def end_round(player_won=False, player_lost=False):
    global wins, losses

    if player_won:
        wins += 1
        wins_label.config(text=f"Wins: {wins}")

    if player_lost:
        losses += 1
        losses_label.config(text=f"Losses: {losses}")

    # Disable Hit and Stand after the round
    hit_button.config(state="disabled")
    stand_button.config(state="disabled")

    
def player_stand():

    dealer_hidden_label.destroy()  # remove hidden card back

    # Show dealer's hidden card
    second_card = dealer_hand[1]
    show_card(second_card, dealer_cards_frame, dealer_card_images)

    # Dealer hits until 17 or more
    while calculate_hand_value(dealer_hand) < 17:
        card = draw_card()
        dealer_hand.append(card)
        show_card(card, dealer_cards_frame, dealer_card_images)

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if dealer_value > 21:
        messagebox.showinfo("Win", "Dealer busts. You win!")
        end_round(player_won=True)
    elif player_value > dealer_value:
        messagebox.showinfo("Win", "You win!")
        end_round(player_won=True)
    elif dealer_value > player_value:
        messagebox.showinfo("Lose", "Dealer wins.")
        end_round(player_lost=True)
    else:
        messagebox.showinfo("Tie", "Push (tie).")
        end_round()  # no win or loss


############################ ROOT WINDOW SET UP ############################
# Start the main window and name it
root = tk.Tk()
root.title("From Addiction Import Blackjack")
root.geometry("800x600") # Window size
root.configure(background = 'green')


# Create container frames
container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)
# Makes sure the container fills the window
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Create all 3 frames
main_menu_frame = tk.Frame(container, bg='green')
game_screen = tk.Frame(container, bg = 'green')
rules_screen = tk.Frame(container, bg = 'green')

for frame in (main_menu_frame, game_screen, rules_screen):
    frame.grid(row=0, column=0, sticky='nsew')




############################## Main Menu Frame ###############################
tk.Label(main_menu_frame, text = 'From Addiction Import Blackjack',
          font=("Impact", 24, "bold"), 
          bg='green').pack(pady=40)

# Buttons on main menu
tk.Button(main_menu_frame, text="Play Blackjack",
          font=("Impact", 16),
          width=20,
          command = goto_game
        ).pack(pady=10)
tk.Button(main_menu_frame, text="Rules", 
          font=("Impact", 16), 
          width=20, 
          command=lambda: show_frame(rules_screen)
          ).pack(pady=10)

tk.Button(main_menu_frame, text="Exit", 
          font=("Impact", 16), 
          width=20,
          command=root.quit
          ).pack(pady=10)

######### Game Screen Frame ############

###### Hidden back card for dealer########
card_back = tk.PhotoImage(file='cards/card_back.png').subsample(3)

# Title
tk.Label(game_screen, text="Blackjack Table", font=("Impact", 26), bg="green").pack(pady=20)

# Dealer section
dealer_frame = tk.Frame(game_screen, bg="green")
dealer_frame.pack(pady=20)

tk.Label(dealer_frame, text="Dealer's Hand", font=("Arial", 16), bg="green").pack()

dealer_cards_frame = tk.Frame(dealer_frame, bg="green")
dealer_cards_frame.pack(pady=10)

# Player section
player_frame = tk.Frame(game_screen, bg="green")
player_frame.pack(pady=20)

tk.Label(player_frame, text="Your Hand", font=("Arial", 16), bg="green").pack()

player_cards_frame = tk.Frame(player_frame, bg="green")
player_cards_frame.pack(pady=10)

# Buttons section
button_frame = tk.Frame(game_screen, bg="green")
button_frame.pack(pady=20)

hit_button = tk.Button(button_frame, text="Hit", width=12, command=player_hit)
hit_button.grid(row=0, column=0, padx=10)
stand_button = tk.Button(button_frame, text="Stand", width=12, command=player_stand)
stand_button.grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Restart", width=12, command=start_round).grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Exit to Menu", width=12,
          command=lambda: show_frame(main_menu_frame)).grid(row=0, column=3, padx=10)

# Win/Loss Counter
stats_frame = tk.Frame(game_screen, bg="green")
stats_frame.pack(pady=30)

wins_label = tk.Label(stats_frame, text="Wins: 0", font=("Arial", 16), bg="green")
losses_label = tk.Label(stats_frame, text="Losses: 0", font=("Arial", 16), bg="green")

wins_label.grid(row=0, column=0, padx=20)
losses_label.grid(row=0, column=1, padx=20)


# Game frame
show_frame(main_menu_frame)
root.mainloop()
