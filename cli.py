# cli.py
import sys
import time
from game import BlackjackGame

# try:
#     import pyfiglet
#     from colorama import init, fore, Style
#     init(autoreset=True)
#     print(Fore.GREEN + pyfiglet.figlet_format("BLACKJACK"))
#     print(Style.DIM + "Type 'q' anytime to quit.")
#
# except Exception:
#     print("=== BLACKJACK ===")


def show_hands(game, reveal_dealer=False):
    p = " ".join(f"{c.rank}{c.suit}" for c in game.player.hand.cards)

    if reveal_dealer:
        d = " ".join(f"{c.rank}{c.suit}" for c in game.dealer.hand.cards)
        d_total = game.dealer.hand.total()

    else:
        up = game.dealer.hand.cards[0]
        d = f"{up.rank}{up.suit} ??"
        d_total = "??"

    print("—————————————————————————————————————————")
    print(f"\nDealer: {d} (total: {d_total})")
    print(f"\nPlayer: {p} (total: {game.player.hand.total()})")
    print(f"Chips: {game.player.chips}\n")
    print("—————————————————————————————————————————")


def main():
    game = BlackjackGame(n_decks=6, delay=0.0)

    while True:
        # Betting
        while True:
            bet = input("Bet amount (or 'q' to quit): ").strip()
            if bet.lower() == "q":
                print("Goodbye!")
                sys.exit(0)

            try:
                bet = int(bet)
                game.new_round(bet)
                break
            except ValueError as e:
                print(f"Invalid bet: {e}")

        show_hands(game, reveal_dealer=False)

        # Player turn
        while True:
            if game.player.hand.is_bust():
                print("You busted!")
                break

            if game.player.hand.is_blackjack():
                print("Blackjack!")
                break

            move = input("[H]it, [S]tand (or 'q'): ").strip().lower()
            if move == "q":
                print("Goodbye!")
                sys.exit(0)

            if move in ("h", "hit"):
                busted = game.player_hit()
                show_hands(game, reveal_dealer=False)

                if busted:
                    print("You busted!")
                    break
            elif move in ("s", "stand"):
                break

            else:
                print("Please type H or S.")

        # Dealer turn
        if not game.player.hand.is_bust():
            print("Dealer plays...")
            time.sleep(0.3)
            game.dealer_play()

        # Debug totals
        # pt = game.player.hand.total()
        # dt = game.player.hand.total()
        # print(f"DEBUG - PLayer total: {pt}, Dealer total: {dt}")

        result = game.resolve()
        show_hands(game, reveal_dealer=True)
        print("Result:", result.replace("_", " ").title())
        print("-" * 32)

        # Prompt to play again
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()