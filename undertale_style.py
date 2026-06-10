import random
import time


def p(text, delay=0.6):
    print(text)
    time.sleep(delay)


def choice(prompt, opts):
    opts_l = [o.lower() for o in opts]
    ans = input(prompt).strip().lower()
    while ans not in opts_l:
        print(f"Options: {', '.join(opts)}")
        ans = input(prompt).strip().lower()
    return ans


def intro():
    p("Welcome to 'Understars' — a short, original, turn-based encounter game.")
    p("This is inspired by turn-based pacifist-or-fight mechanics, but uses original characters and text.")


def make_player():
    return {"hp": 20, "max_hp": 20, "inventory": {"medkit": 1}, "mercy_points": 0}


def make_boss():
    return {
        "name": "Guardian of the Hollow",
        "hp": 35,
        "phase": 1,
        "resolve": 10,  # higher means harder to pacify
        "angry": False,
    }


def show_status(player, boss):
    p(f"You HP: {player['hp']}/{player['max_hp']} | Boss HP: {boss['hp']} | Boss resolve: {boss['resolve']}")


def player_fight(player, boss):
    # simple attack with variable damage
    dmg = random.randint(2, 6)
    boss['hp'] -= dmg
    p(f"You strike the {boss['name']} for {dmg} damage.")


def player_act(player, boss):
    p("You try to ACT. Choose a non-violent action to influence the boss.")
    act = choice("Act (compliment/joke/dance): ", ["compliment", "joke", "dance"]) 
    if act == "compliment":
        p("You compliment the boss's ancient helmet. It hesitates.")
        boss['resolve'] = max(0, boss['resolve'] - 2)
        player['mercy_points'] += 1
    elif act == "joke":
        p("You tell a silly joke. The boss emits a short, confused chuckle.")
        if random.random() < 0.6:
            boss['resolve'] = max(0, boss['resolve'] - 1)
            player['mercy_points'] += 1
        else:
            p("The joke falls flat.")
    else:
        p("You perform an awkward little dance. The boss blinks.")
        if random.random() < 0.5:
            boss['resolve'] = max(0, boss['resolve'] - 3)
            player['mercy_points'] += 2


def player_item(player, boss):
    if player['inventory'].get('medkit', 0) > 0:
        player['hp'] = min(player['max_hp'], player['hp'] + 8)
        player['inventory']['medkit'] -= 1
        p("You use a medkit and restore 8 HP.")
    else:
        p("No medkits left.")


def player_mercy(player, boss):
    # Mercy succeeds if boss resolve low or mercy_points high
    chance = 0.2 + (max(0, 10 - boss['resolve']) * 0.06) + (player['mercy_points'] * 0.05)
    if random.random() < chance:
        p(f"You spare the {boss['name']}. It calms and lets you pass peacefully.")
        boss['hp'] = 0
    else:
        p("Mercy fails. The boss is not convinced.")
        boss['resolve'] += 1


def boss_action(player, boss):
    # boss acts differently by phase
    if boss['phase'] == 1:
        p(f"{boss['name']} launches a slow spectral swipe!")
        dmg = random.randint(2, 4)
        player['hp'] -= dmg
        p(f"You take {dmg} damage.")
    else:
        move = random.choice(["Shadow Volley", "Hollow Charge", "Echo Beam"])
        p(f"{boss['name']} uses {move}!")
        if move == "Shadow Volley":
            hits = random.randint(2, 3)
            total = 0
            for _ in range(hits):
                d = random.randint(1, 3)
                total += d
                player['hp'] -= d
            p(f"Shadow Volley hits {hits} times for {total} damage.")
        elif move == "Hollow Charge":
            d = random.randint(4, 7)
            player['hp'] -= d
            p(f"You are slammed for {d} damage.")
        else:
            # Echo Beam: reduces mercy points
            p("An eerie beam reduces your confidence.")
            player['mercy_points'] = max(0, player['mercy_points'] - 1)


def check_phase(boss):
    if boss['hp'] <= 20 and boss['phase'] == 1:
        boss['phase'] = 2
        boss['resolve'] += 4
        p(f"{boss['name']} becomes enraged and shifts into Phase 2!")


def play():
    intro()
    player = make_player()
    boss = make_boss()

    while player['hp'] > 0 and boss['hp'] > 0:
        show_status(player, boss)
        act = choice("Choose action (fight/act/item/mercy): ", ["fight", "act", "item", "mercy"])
        if act == 'fight':
            player_fight(player, boss)
        elif act == 'act':
            player_act(player, boss)
        elif act == 'item':
            player_item(player, boss)
        else:
            player_mercy(player, boss)

        if boss['hp'] <= 0:
            break

        # boss turn
        check_phase(boss)
        boss_action(player, boss)

    if player['hp'] <= 0:
        p("You fell... but determination lives on. Try again.")
    else:
        p("Victory — you resolved the conflict without unnecessary harm!")


def main():
    while True:
        play()
        again = choice("Play again? (yes/no): ", ["yes", "no"])
        if again == 'no':
            p("Thanks for playing Understars!")
            break


if __name__ == '__main__':
    main()
