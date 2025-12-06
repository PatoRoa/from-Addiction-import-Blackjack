import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import os
import json
from deck import Deck
from card import Card



#function to switch screens
def show_frame(frame):
    frame.tkraise() #bring the frame to the front


########################### BlackJack Game CLass ##############################
class BlackjackGame:
    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []
        self.player_images = []
        self.dealer_images = []
        self.wins = 0
        self.losses = 0
        self.deck = None
        self.hidden_label = None
        self.load_stats()

    def start_round(self):

        # New shuffled deck
        self.deck = Deck()
        self.deck.shuffle()

        # Clear hands and images
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.player_images.clear()
        self.dealer_images.clear()

        # Clear GUI card frames
        for widget in player_cards_frame.winfo_children():
            widget.destroy()

        for widget in dealer_cards_frame.winfo_children():
            widget.destroy()

        # Deal player cards
        c1 = self.deck.draw()
        c2 = self.deck.draw()
        self.player_hand.extend([c1, c2])
        show_card(c1, player_cards_frame, self.player_images)
        show_card(c2, player_cards_frame, self.player_images)

        # Automatic blackjack check
        if calculate_hand_value(self.player_hand) == 21:
            messagebox.showinfo("Blackjack!", "You got a Blackjack! You win!")
            self.end_round(player_won=True)
            return

        # Dealer cards
        d1 = self.deck.draw()
        d2 = self.deck.draw()
        self.dealer_hand.extend([d1, d2])

        show_card(d1, dealer_cards_frame, self.dealer_images)

        # Face-down card
        self.hidden_label = tk.Label(dealer_cards_frame, image=card_back, bg="green")
        self.hidden_label.pack(side="left")

        hit_button.config(state="normal")
        stand_button.config(state="normal")
    
    def player_hit(self):
        card = self.deck.draw()
        self.player_hand.append(card)
        show_card(card, player_cards_frame, self.player_images)

        if calculate_hand_value(self.player_hand) > 21:
            messagebox.showinfo("Bust", "You busted! Dealer wins.")
            self.end_round(player_lost=True)

    def player_stand(self):
        # Reveal hidden card
        self.hidden_label.destroy()

        second_card = self.dealer_hand[1]
        show_card(second_card, dealer_cards_frame, self.dealer_images)

        # Dealer hits until 17+
        while calculate_hand_value(self.dealer_hand) < 17:
            card = self.deck.draw()
            self.dealer_hand.append(card)
            show_card(card, dealer_cards_frame, self.dealer_images)

        player_value = calculate_hand_value(self.player_hand)
        dealer_value = calculate_hand_value(self.dealer_hand)

        if dealer_value > 21:
            messagebox.showinfo("Win", "Dealer busts. You win!")
            self.end_round(player_won=True)

        elif player_value > dealer_value:
            messagebox.showinfo("Win", "You win!")
            self.end_round(player_won=True)

        elif dealer_value > player_value:
            messagebox.showinfo("Lose", "Dealer wins.")
            self.end_round(player_lost=True)

        else:
            messagebox.showinfo("Tie", "Push (tie).")
            self.end_round()

    def end_round(self, player_won=False, player_lost=False):
        if player_won:
            self.wins += 1
            wins_label.config(text=f"Wins: {self.wins}")

        if player_lost:
            self.losses += 1
            losses_label.config(text=f"Losses: {self.losses}")
        
        #saving score
        self.save_stats()

        # Disable buttons
        hit_button.config(state="disabled")
        stand_button.config(state="disabled")

    def load_stats(self):
        if os.path.exists("stats.json"):
            with open("stats.json", "r") as f:
                data = json.load(f)
                self.wins = data.get("wins", 0)
                self.losses = data.get("losses", 0)

    def save_stats(self):
        data = {"wins": self.wins, "losses": self.losses}
        with open("stats.json", "w") as f:
            json.dump(data, f)
                    
    def update_stats_labels(self):
        wins_label.config(text=f"Wins: {self.wins}")
        losses_label.config(text=f"Losses: {self.losses}")




############################## CARD FUNCTIONS ##############################


def show_card(card, frame, image_list):
    filename = card.filename()
    img = tk.PhotoImage(file=filename).subsample(3)

    image_list.append(img)  # prevent garbage collection

    label = tk.Label(frame, image=img, bg="green")
    label.pack(side="left")

############################# Value Counting ####################################
def calculate_hand_value(hand):
    value = 0
    aces = 0

    for card in hand:
        rank = card.rank

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

game = BlackjackGame()


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
          command=lambda: [show_frame(game_screen), game.start_round()]
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

############ Rules Screen Frame ############
# Rules title Label
tk.Label(rules_screen, text="How to play Blackjack",
         font=("Impact", 24, "bold"),
         bg='green').pack(pady=0, fill="x")

# Rules text Text
rules = """
• The goal of Blackjack is to beat the dealer's hand without scoring over 21 in your hand
• Cards 2 through 10 are worth their rank in points, Jacks, Queens and Kings are worth 10, and Aces are worth either 1 or 11
• The dealer deals a card to you and themselves, then deals the second card, turning theirs face-down
• You can decide to stay and run your chances or Hit to potentially score closer to 21
• Whoever scores higher than 21 at any point Busts and loses
• Whoever scores exactly 21 at any point automatically wins
• If both you and the dealer score the same, it's a Push; no one wins or loses
• For best results, wash before use and involve real-world money*

*The TakeYourMoneyAndRun Corporation is not responsible for any irresponsibility.
"""
tk.Label(rules_screen,
         anchor="nw",
         text=rules,
         font=("Arial", 15),
         justify="left",
         wraplength=750
         ).pack(pady=40, padx=20, fill="both", expand=False)

# Hitting the griddy

# Back to Main Menu button
tk.Button(rules_screen, text="Main Menu",
          font=("Impact", 24),
          width=20,
          command=lambda: show_frame(main_menu_frame)).pack(pady=10)

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

hit_button = tk.Button(button_frame, text="Hit", width=12, command=lambda: game.player_hit())
hit_button.grid(row=0, column=0, padx=10)
stand_button = tk.Button(button_frame, text="Stand", width=12, command=lambda: game.player_stand())
stand_button.grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Restart", width=12, command=lambda: game.start_round()).grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Exit to Menu", width=12,
          command=lambda: show_frame(main_menu_frame)).grid(row=0, column=3, padx=10)

# Win/Loss Counter
stats_frame = tk.Frame(game_screen, bg="green")
stats_frame.pack(pady=30)

wins_label = tk.Label(stats_frame, text="Wins: 0", font=("Arial", 16), bg="green")
losses_label = tk.Label(stats_frame, text="Losses: 0", font=("Arial", 16), bg="green")

wins_label.grid(row=0, column=0, padx=20)
losses_label.grid(row=0, column=1, padx=20)

game.update_stats_labels()



# Game frame
show_frame(main_menu_frame)
root.mainloop()
