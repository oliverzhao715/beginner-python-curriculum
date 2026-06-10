import random
import time


def pr(text, delay=0.6):
    print(text)
    time.sleep(delay)


def choice(prompt, opts):
    optset = [o.lower() for o in opts]
    ans = input(prompt).strip().lower()
    while ans not in optset:
        print(f"Choose: {', '.join(opts)}")
        ans = input(prompt).strip().lower()
    return ans


def intro():
    pr("Welcome to Meme Shooter: Boss Rush!")
    pr("You face the ULTIMATE MEME BOSS. Use silly weapons and win.")


def make_player():
    return {
        "health": 20,
        "medkits": 1,
        "weapons": {
            "ak47": {"damage": (2, 4), "desc": "Rapid-fire AK (consistent damage)"},
            "sticky grenade": {"damage": (3, 3), "desc": "Sticks and deals DOT"},
            "rubber chicken": {"damage": (1, 3), "desc": "Chance to stun the boss (meme chaos)"},
            "memeflare": {"damage": (6, 12), "desc": "High damage but low accuracy"},
        },
        "sticky_on_boss": 0,  # turns of DOT on boss
    }


def make_boss():
    return {
        "name": "The Meme Overlord",
        "health": 45,
        "shield": 0,  # temporary damage reduction
        "stunned": 0,
        "moves": ["T-Pose Slam", "Pepe Shield", "Dab Barrage", "Rickroll Riposte"],
    }


def player_attack(player, boss, weapon):
    w = player["weapons"][weapon]
    lo, hi = w["damage"]
    if weapon == "memeflare":
        # low accuracy
        if random.random() < 0.5:
            dmg = random.randint(lo, hi)
        else:
            pr("Memeflare misfired! No damage.")
            return
    elif weapon == "sticky grenade":
        dmg = random.randint(lo, hi)
        pr("Sticky grenade sticks to the boss and will burn for 2 turns.")
        boss["sticky"] = 2
        boss["sticky_dmg"] = 2
    elif weapon == "rubber chicken":
        dmg = random.randint(lo, hi)
        if random.random() < 0.35:
            pr("The chicken's slap stunned the boss!")
            boss["stunned"] = 1
    else:  # ak47
        dmg = random.randint(lo, hi)

    # apply shield reduction
    actual = max(0, dmg - boss.get("shield", 0))
    boss["health"] -= actual
    pr(f"You hit the boss for {actual} damage.")


def boss_turn(player, boss):
    if boss.get("stunned", 0) > 0:
        pr("Boss is stunned and skips its turn!")
        boss["stunned"] -= 1
        return

    move = random.choice(boss["moves"])
    pr(f"Boss uses {move}!")
    if move == "T-Pose Slam":
        dmg = random.randint(3, 6)
        player["health"] -= dmg
        pr(f"You take {dmg} damage from the slam.")
    elif move == "Pepe Shield":
        boss["shield"] = 2
        pr("Boss raises a Pepe Shield, reducing damage next turn.")
    elif move == "Dab Barrage":
        hits = random.randint(2, 4)
        total = 0
        for _ in range(hits):
            d = random.randint(1, 3)
            total += d
            player["health"] -= d
        pr(f"Dab Barrage hits you {hits} times for {total} total damage.")
    else:  # Rickroll Riposte
        pr("Boss rickrolls you — you lose focus and drop energy (no damage, slight stun).")
        if random.random() < 0.4:
            boss["stunned"] = 0
            pr("But you're too embarrassed to act for a moment.")


def apply_effects(player, boss):
    # sticky DOT
    if boss.get("sticky", 0) > 0:
        boss["sticky"] -= 1
        dmg = boss.get("sticky_dmg", 0)
        boss["health"] -= dmg
        pr(f"Sticky grenade burns boss for {dmg} damage.")
    # reduce shield after it had effect for one turn
    if boss.get("shield", 0) > 0:
        boss["shield"] = max(0, boss["shield"] - 1)


def play_shooter():
    intro()
    player = make_player()
    boss = make_boss()

    while player["health"] > 0 and boss["health"] > 0:
        pr(f"Your HP: {player['health']} | Boss HP: {boss['health']}")
        pr("Weapons: ak47, sticky grenade, rubber chicken, memeflare")
        pr(f"Medkits: {player['medkits']}")
        act = choice("Action (fire/use/inspect): ", ["fire", "use", "inspect"])
        if act == "inspect":
            pr("Inspecting boss...")
            pr(f"Boss state: shield={boss.get('shield',0)} stunned={boss.get('stunned',0)}")
            continue
        if act == "use":
            if player["medkits"] > 0:
                player["health"] += 6
                player["medkits"] -= 1
                pr("You use a medkit and regain 6 HP.")
            else:
                pr("No medkits left!")
            # boss may still act
        else:  # fire
            w = choice("Choose weapon: ", ["ak47", "sticky grenade", "rubber chicken", "memeflare"])
            player_attack(player, boss, w)

        # apply ongoing effects
        apply_effects(player, boss)

        if boss["health"] <= 0:
            break

        # boss action
        boss_turn(player, boss)

    if player["health"] <= 0:
        pr("You were defeated by the Meme Overlord. Try again.")
    else:
        pr("The Meme Overlord has been vanquished! You win the meme war!")


def main():
    while True:
        play_shooter()
        again = choice("Play again? (yes/no): ", ["yes", "no"])
        if again == "no":
            pr("Thanks for playing Meme Shooter!")
            break


if __name__ == "__main__":
    main()
