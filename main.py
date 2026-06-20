import time

from echo_labyrinth import play_labyrinth
from mystic_market import play_market
from shooter_game import play_shooter
from text_game import play_game
from undertale_text_game import battle


def print_pause(message, delay=0.5):
    print(message)
    time.sleep(delay)


def get_choice(prompt, options):
    answer = input(prompt).strip().lower()
    while answer not in options:
        print(f"Choose one of: {', '.join(options)}")
        answer = input(prompt).strip().lower()
    return answer


def show_hub_menu():
    print("\n=== MINIGAME HUB ===")
    print("1) Hollow Heart - turn-based encounter")
    print("2) Meme Shooter - silly boss fight")
    print("3) Star Horizon Patrol - space text adventure")
    print("4) Mystic Market - magical trading game")
    print("5) Echo Labyrinth - echo-based maze")
    print("6) Quit")


def main():
    while True:
        show_hub_menu()
        choice = get_choice("Choose a minigame (1/2/3/4/5/6): ", ["1", "2", "3", "4", "5", "6"])
        if choice == "1":
            battle()
        elif choice == "2":
            play_shooter()
        elif choice == "3":
            play_game()
        elif choice == "4":
            play_market()
        elif choice == "5":
            play_labyrinth()
        else:
            print("Goodbye from the Minigame Hub!")
            break


if __name__ == "__main__":
    import time
    main()
