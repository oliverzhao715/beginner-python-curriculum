import random
import time


def print_pause(message, delay=0.8):
    print(message)
    time.sleep(delay)


def get_choice(prompt, choices):
    choice = input(prompt).strip().lower()
    while choice not in choices:
        print(f"Please choose one of: {', '.join(choices)}")
        choice = input(prompt).strip().lower()
    return choice


def show_status(player):
    print_pause("--- COMMAND HUD ---")
    print_pause(f"Hull Integrity: {player['health']}")
    print_pause(f"Energy Cells: {player['energy']}")
    print_pause(f"Credits: {player['credits']}")
    print_pause(f"Weapons: {', '.join(player['weapons']) if player['weapons'] else 'None'}")
    print_pause(f"Mission Day: {player['day']}")
    print_pause("-------------------", delay=0.3)


def intro():
    print_pause("Welcome aboard the starship Horizon.")
    print_pause("The galaxy is in peril. A stolen quantum core is hidden on the planet Vex-9.")
    print_pause("Your goal: recover the core, escape the alien moon, and return to the spaceport." )


def space_station(player):
    print_pause("You dock at the Orion Space Bazaar.")
    while True:
        print_pause("Available gear:")
        print_pause("1) Nano-med pack (4 credits)")
        print_pause("2) Laser rifle upgrade (6 credits)")
        print_pause("3) Plasma shields (5 credits)")
        print_pause("4) Launch ship")
        choice = get_choice("Buy what? (1/2/3/4): ", ["1", "2", "3", "4"])
        if choice == "4":
            print_pause("You leave the station to continue your mission.")
            break
        if choice == "1" and player["credits"] >= 4:
            player["credits"] -= 4
            player["inventory"].append("med pack")
            print_pause("Nano-med pack added to your inventory.")
        elif choice == "2" and player["credits"] >= 6:
            if "laser rifle" in player["weapons"]:
                print_pause("You already have the rifle upgrade.")
            else:
                player["credits"] -= 6
                player["weapons"].append("laser rifle")
                print_pause("Your laser gun is now upgraded.")
        elif choice == "3" and player["credits"] >= 5:
            if player["shielded"]:
                print_pause("Your shields are already active.")
            else:
                player["credits"] -= 5
                player["shielded"] = True
                print_pause("Plasma shields are activated.")
        else:
            print_pause("Not enough credits or already equipped.")


def planet_surface(player):
    print_pause("You land on Vex-9 and step into its glowing alien forest.")
    # track repeated visits so the keycard isn't pure bad luck
    player["planet_visits"] = player.get("planet_visits", 0) + 1
    if not player["found_transponder"]:
        print_pause("A crashed drone flashes nearby.")
        if get_choice("Investigate the drone? (yes/no): ", ["yes", "no"]) == "yes":
            print_pause("Inside you find a transponder beacon.")
            player["found_transponder"] = True
            player["inventory"].append("transponder")
        else:
            print_pause("You leave the drone and move deeper into the forest.")
    else:
        print_pause("You move carefully through the forest,")
    if not player["found_keycard"]:
        # guarantee after 3 visits, otherwise 50% chance
        if player.get("planet_visits", 0) >= 3 or random.choice([True, False]):
            print_pause("You discover a hidden alien cache containing a keycard.")
            player["found_keycard"] = True
            player["inventory"].append("keycard")
        else:
            print_pause("A giant insect screeches, but you avoid it.")
    else:
        print_pause("You recall the forest paths and avoid danger.")


def lunar_caves(player):
    print_pause("The lunar caves pulse with ultraviolet light.")
    if not player["night_vision"]:
        print_pause("Without night vision it's almost impossible to see.")
        if random.choice([True, False]):
            print_pause("You fall and scrape your armor.")
            player["health"] -= 1
        else:
            print_pause("You move slowly and avoid the shadows.")
    else:
        print_pause("Your night vision reveals hidden tunnels.")
    if player["found_transponder"]:
        print_pause("Your transponder detects a hidden passage ahead.")
        if not player["discovered_base"]:
            print_pause("You find the entrance to an underground alien base.")
            player["discovered_base"] = True
        else:
            print_pause("You return to the alien base entrance.")
    else:
        print_pause("The cave holds strange crystals, but no base entrance.")


def alien_base(player):
    if not player["discovered_base"]:
        print_pause("You can't locate the alien base from here.")
        return
    if player["core_retrieved"]:
        print_pause("The quantum core is already secured. Fly back to the spaceport.")
        return
    print_pause("The base door is sealed by alien tech.")
    if "keycard" not in player["inventory"]:
        print_pause("You need a keycard to bypass the door.")
        return
    print_pause("You swipe the keycard and the door powers down.")
    print_pause("A defense drone scans the room and fires.")
    survived = combat(player, "defense drone", 6)
    if survived:
        print_pause("You reach the core chamber.")
        print_pause("A holographic sentinel asks a challenge:")
        print_pause("'What runs but never walks, has a mouth but never talks?' ")
        answer = input("Answer: ").strip().lower()
        if answer == "river":
            print_pause("The sentinel steps aside and lets you take the quantum core.")
            player["core_retrieved"] = True
            player["inventory"].append("quantum core")
        else:
            print_pause("The sentinel rejects your answer and overloads the room.")
            player["health"] -= 2
            if player["health"] > 0:
                print_pause("You escape the base wounded.")


def combat(player, enemy, enemy_health):
    print_pause(f"An enemy {enemy} engages your ship!")
    while enemy_health > 0 and player["health"] > 0:
        print_pause(f"Hull: {player['health']} | Energy: {player['energy']} | {enemy} power: {enemy_health}")
        action = get_choice("Fire or evade? (fire/evade): ", ["fire", "evade"])
        if action == "fire":
            if "laser rifle" in player["weapons"]:
                damage = random.randint(2, 5)
            else:
                damage = random.randint(1, 3)
            enemy_health -= damage
            print_pause(f"Your lasers hit for {damage} damage.")
            if enemy_health <= 0:
                print_pause(f"You destroy the {enemy}!")
                player["credits"] += 5
                player["energy"] -= 1
                return True
            enemy_damage = random.randint(1, 3)
            shield = 1 if player["shielded"] else 0
            player["health"] -= max(0, enemy_damage - shield)
            print_pause(f"The {enemy} hits your hull for {max(0, enemy_damage - shield)} damage.")
        else:
            if random.choice([True, False]):
                print_pause("You evade successfully.")
                player["energy"] -= 1
                return True
            else:
                print_pause("Evade failed, the enemy fires.")
                enemy_damage = random.randint(1, 3)
                player["health"] -= enemy_damage
                print_pause(f"You take {enemy_damage} damage.")
    return player["health"] > 0


def random_event(player):
    if random.choice([True, False]):
        print_pause("A pirate skiff appears from the nebula.")
        combat(player, "pirate skiff", 5)
    else:
        print_pause("The route stays calm as you transit.")


def check_game_status(player):
    if player["health"] <= 0:
        print_pause("Your ship has been destroyed.")
        return "lost"
    if player["core_retrieved"] and player["location"] == "spaceport":
        print_pause("You dock at the spaceport with the quantum core.")
        return "won"
    if player["day"] >= 8 and not player["core_retrieved"]:
        print_pause("The mission timer expires and the enemy reinforcements arrive.")
        return "lost"
    if player["energy"] <= 0:
        print_pause("Your ship's energy cells are depleted.")
        return "lost"
    return "continue"


def player_action(player):
    player["day"] += 1
    if player["location"] == "spaceport":
        print_pause("Command console ready. Choose your next move.")
        print_pause("Options: station, planet, caves, base, status, quit")
        choice = get_choice(
            "What do you do? (station/planet/caves/base/status/quit): ",
            ["station", "planet", "caves", "base", "status", "quit"],
        )
        if choice == "station":
            space_station(player)
        elif choice == "planet":
            player["location"] = "planet"
            planet_surface(player)
        elif choice == "caves":
            player["location"] = "caves"
            lunar_caves(player)
        elif choice == "base":
            player["location"] = "base"
            alien_base(player)
        elif choice == "status":
            show_status(player)
        else:
            player["health"] = 0
            print_pause("You abort the mission.")
    else:
        print_pause(f"You return to the spaceport from the {player['location']}.")
        if random.choice([True, False]):
            random_event(player)
        player["location"] = "spaceport"


def play_game():
    player = {
        "health": 8,
        "energy": 5,
        "credits": 12,
        "weapons": ["laser pistol"],
        "inventory": [],
        "shielded": False,
        "night_vision": False,
        "planet_visits": 0,
        "found_transponder": False,
        "found_keycard": False,
        "discovered_base": False,
        "core_retrieved": False,
        "location": "spaceport",
        "day": 0,
    }
    intro()
    while True:
        status = check_game_status(player)
        if status != "continue":
            break
        player_action(player)
    if status == "won":
        print_pause("Mission complete! The galaxy is safe once again.")
    else:
        print_pause("Mission failed. The quantum core remains missing.")


def main():
    while True:
        play_game()
        again = get_choice("Launch another mission? (yes/no): ", ["yes", "no"])
        if again == "no":
            print_pause("Thanks for playing Star Horizon Patrol!")
            break


if __name__ == "__main__":
    main()
