import random
import time


def print_pause(message, delay=0.6):
    print(message)
    time.sleep(delay)


def get_choice(prompt, options):
    answer = input(prompt).strip().lower()
    while answer not in options:
        print(f"Choose one of: {', '.join(options)}")
        answer = input(prompt).strip().lower()
    return answer


def intro():
    print_pause("Welcome to Hollow Heart: a short text-based encounter game.")
    print_pause("You are a traveler in a strange forest, facing a mysterious guardian.")
    print_pause("Your choices will decide whether you fight or show mercy.")


def make_player():
    return {
        "hp": 18,
        "max_hp": 18,
        "medkits": 2,
        "mercy": 0,
    }


def make_enemy():
    return {
        "name": "Forest Guardian",
        "hp": 25,
        "resolve": 10,
    }


def show_status(player, enemy):
    print_pause(f"\nYou HP: {player['hp']}/{player['max_hp']} | {enemy['name']} HP: {enemy['hp']} | Resolve: {enemy['resolve']}", 0.3)


def player_attack(player, enemy):
    damage = random.randint(3, 6)
    enemy['hp'] -= damage
    print_pause(f"You attack and deal {damage} damage.")


def player_act(player, enemy):
    print_pause("You try to ACT. Choose a kind action to calm the guardian.")
    choice = get_choice("Act: compliment / joke / dance: ", ["compliment", "joke", "dance"])
    if choice == "compliment":
        print_pause("You compliment the guardian's glowing eyes.")
        enemy['resolve'] = max(0, enemy['resolve'] - 2)
        player['mercy'] += 1
    elif choice == "joke":
        print_pause("You tell a silly joke.")
        if random.random() < 0.7:
            print_pause("The guardian smiles faintly.")
            enemy['resolve'] = max(0, enemy['resolve'] - 1)
            player['mercy'] += 1
        else:
            print_pause("The guardian does not seem amused.")
    else:
        print_pause("You begin to dance in a goofy way.")
        if random.random() < 0.5:
            print_pause("The guardian tilts its head, softened by your dance.")
            enemy['resolve'] = max(0, enemy['resolve'] - 3)
            player['mercy'] += 2
        else:
            print_pause("The guardian watches quietly.")


def player_item(player, enemy):
    if player['medkits'] > 0:
        player['hp'] = min(player['max_hp'], player['hp'] + 8)
        player['medkits'] -= 1
        print_pause("You use a medkit and recover 8 HP.")
    else:
        print_pause("No medkits left.")


def player_mercy(player, enemy):
    chance = 0.15 + (max(0, 10 - enemy['resolve']) * 0.05) + (player['mercy'] * 0.05)
    print_pause(f"You attempt MERCY (success chance {int(chance * 100)}%).")
    if random.random() < chance:
        print_pause(f"The {enemy['name']} calms and accepts your mercy.")
        enemy['hp'] = 0
    else:
        print_pause("Mercy fails. The guardian is not ready yet.")
        enemy['resolve'] = min(20, enemy['resolve'] + 2)


def enemy_turn(player, enemy):
    if enemy['hp'] <= 0:
        return
    attack = random.choice(["slap", "swipe", "gaze"])
    if attack == "slap":
        damage = random.randint(2, 4)
        print_pause("The guardian slaps you with a wispy vine.")
    elif attack == "swipe":
        damage = random.randint(3, 5)
        print_pause("The guardian sweeps its branch toward you.")
    else:
        damage = random.randint(1, 3)
        print_pause("The guardian stares into your eyes, unsettling your spirit.")
    player['hp'] -= damage
    print_pause(f"You take {damage} damage.")


def battle():
    intro()
    player = make_player()
    enemy = make_enemy()

    while player['hp'] > 0 and enemy['hp'] > 0:
        show_status(player, enemy)
        action = get_choice("Choose action (fight/act/item/mercy): ", ["fight", "act", "item", "mercy"])
        if action == "fight":
            player_attack(player, enemy)
        elif action == "act":
            player_act(player, enemy)
        elif action == "item":
            player_item(player, enemy)
        else:
            player_mercy(player, enemy)

        if enemy['hp'] <= 0:
            break

        enemy_turn(player, enemy)

    if player['hp'] <= 0:
        print_pause("You were defeated. Determination fades, but you can try again.")
    else:
        if enemy['resolve'] <= 3:
            print_pause("You won the encounter peacefully and earned a true pacifist ending.")
        else:
            print_pause("You defeated the guardian in battle. The path ahead opens.")


def main():
    while True:
        battle()
        again = get_choice("Play again? (yes/no): ", ["yes", "no"])
        if again == "no":
            print_pause("Thanks for playing Hollow Heart!")
            break


if __name__ == "__main__":
    main()
