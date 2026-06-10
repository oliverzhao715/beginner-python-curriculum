import random
import time
import sys
import tty
import termios
import select
try:
    import curses
except Exception:
    curses = None


def delay_print(s, t=0.6):
    print(s)
    time.sleep(t)


def ask_choice(prompt, options):
    opts = [o.lower() for o in options]
    ans = input(prompt).strip().lower()
    while ans not in opts:
        print("Options:", ", ".join(options))
        ans = input(prompt).strip().lower()
    return ans


def header():
    delay_print("=== UNDERSTARS: Expanded Encounter ===", 0.5)
    delay_print("(Original mechanics inspired by turn-based 'ACT' combat, all characters and text are original.)", 0.5)


def make_player():
    return {
        "hp": 24,
        "max_hp": 24,
        "items": {"medkit": 1, "snack": 2, "shield": 1},
        "acts_done": 0,
        "kills": 0,
        "mercies": 0,
    }


def make_boss():
    return {
        "name": "The Hollow Guardian",
        "hp": 60,
        "phase": 1,
        "mood": 50,  # lower => easier to spare
        "dialogue": {
            1: [
                "...You have arrived, little one.",
                "I remember when the hollow was quiet.",
                "This place was never meant for the living.",
            ],
            2: [
                "You persist. Foolish creature.",
                "My patience thins.",
                "You test me; I will respond.",
            ],
            3: [
                "So much light... burns me away.",
                "You will not leave unchanged.",
                "There is no turning back now.",
            ],
        },
        "attacks": {
            1: [
                {"name": "sweep", "text": "A sweeping branch arcs toward you.", "min": 2, "max": 5, "dodge": "chance"},
                {"name": "poke", "text": "A tired claw reaches out to poke.", "min": 1, "max": 3, "dodge": "chance"},
            ],
            2: [
                    {"name": "shards", "text": "Echo shards fly from one side to the other.", "min": 3, "max": 6, "dodge": "direction"},
                    {"name": "spikes", "text": "Spikes burst up from the ground!", "min": 3, "max": 7, "dodge": "lanes"},
                {"name": "burst", "text": "A burst of hollow light seeks a gap in your guard.", "min": 2, "max": 5, "dodge": "chance"},
            ],
            3: [
                    {"name": "onslaught", "text": "A furious onslaught of shards and blows!", "min": 4, "max": 8, "dodge": "chance"},
                    {"name": "focused", "text": "A concentrated spear of light homes in on you.", "min": 5, "max": 9, "dodge": "chance"},
                    {"name": "vine_laser", "text": "Spiky vines fire laser-like tendrils across the field!", "min": 4, "max": 9, "dodge": "lanes"},
            ],
        },
    }


def show_status(player, boss):
    delay_print(f"You HP: {player['hp']}/{player['max_hp']} | {boss['name']} HP: {boss['hp']} | Phase: {boss['phase']}")


def act_menu(player, boss):
    delay_print("ACT options: compliment / reminisce / taunt / sing / inspect")
    a = ask_choice("Choose ACT: ", ["compliment", "reminisce", "taunt", "sing", "inspect"])
    player['acts_done'] += 1
    if a == 'compliment':
        delay_print("You admire the guardian's worn crest. It's quieter now.")
        boss['mood'] = max(0, boss['mood'] - 10)
    elif a == 'reminisce':
        delay_print("You tell a small story of happier hollow days. The guardian's eyes soften.")
        boss['mood'] = max(0, boss['mood'] - 6)
        player['hp'] = min(player['max_hp'], player['hp'] + 2)
    elif a == 'taunt':
        delay_print("You mock the guardian's ancient stance. It flares up in anger.")
        boss['mood'] = min(100, boss['mood'] + 8)
        # taunting makes next hint slightly more obvious
        player['acts_done'] += 0  # no-op to keep tracking
    else:
        if a == 'sing':
            delay_print("You sing a shaky tune. It echoes oddly.")
            if random.random() < 0.5:
                boss['mood'] = max(0, boss['mood'] - 6)
            else:
                delay_print("The tune jars your nerves instead.")
                player['hp'] = max(0, player['hp'] - 2)
        else:
            # inspect
            delay_print("You study the guardian's stance carefully and notice a tell for the next move.")
            player['next_hint'] = True


def fight(player, boss):
    dmg = random.randint(3, 7)
    boss['hp'] -= dmg
    delay_print(f"You attack and deal {dmg} damage.")
    player['kills'] += 0  # track per-battle if needed


def item(player, boss):
    delay_print("Items: medkit / snack / shield / nothing")
    it = ask_choice("Use item: ", ["medkit", "snack", "shield", "nothing"])
    if it == 'medkit':
        if player['items'].get('medkit', 0) > 0:
            player['hp'] = min(player['max_hp'], player['hp'] + 10)
            player['items']['medkit'] -= 1
            delay_print("You use a medkit and heal 10 HP.")
        else:
            delay_print("No medkits left.")
    elif it == 'snack':
        if player['items'].get('snack', 0) > 0:
            player['hp'] = min(player['max_hp'], player['hp'] + 4)
            player['items']['snack'] -= 1
            delay_print("You eat a snack and recover 4 HP.")
        else:
            delay_print("No snacks left.")
    elif it == 'shield':
        if player['items'].get('shield', 0) > 0:
            player['items']['shield'] -= 1
            player['shield_turns'] = player.get('shield_turns', 0) + 1
            delay_print("You brace a spectral shield; it will reduce the next attack.")
        else:
            delay_print("No shields left.")
    else:
        delay_print("You do nothing.")


def mercy(player, boss):
    # success chance increases as mood lowers and with acts
    base = 0.12
    mood_factor = max(0, (60 - boss['mood']) / 100)
    act_factor = min(0.3, player['acts_done'] * 0.05)
    chance = base + mood_factor + act_factor
    delay_print(f"You attempt MERCY (chance {int(chance*100)}%).")
    if random.random() < chance:
        delay_print(f"{boss['name']} calms and accepts mercy.")
        boss['hp'] = 0
        player['mercies'] += 1
    else:
        delay_print("Mercy failed; the guardian is not ready.")
        boss['mood'] = min(100, boss['mood'] + 6)


def boss_attack(player, boss):
    # choose an attack from the phase pool
    pool = boss.get('attacks', {}).get(boss['phase'], [])
    if not pool:
        return
    attack = random.choice(pool)
    delay_print(f"{boss['name']} - {attack['text']}")

    # small ASCII animations to make attacks feel alive
    try:
        attack_name = attack.get('name')
        if attack.get('dodge') == 'direction':
            # animate shards approaching from a side (pass attack name)
            animate_shards_preview(attack_name=attack_name)
        else:
            animate_onslaught_preview(boss['phase'], attack_name=attack_name)
    except Exception:
        # if terminal doesn't support animation, ignore
        pass

    dodge_type = attack.get('dodge', 'chance')
    if dodge_type == 'direction':
        # direction dodge: correct side avoids damage
        correct = random.choice(["left", "right"])
        # compute hint probability (improves with Acts and lower boss mood)
        hint_prob = 0.5 + min(0.35, player.get('acts_done', 0) * 0.05) + max(0, (60 - boss.get('mood', 50)) / 200)
        hint_prob = min(0.95, hint_prob)
        # if player used 'inspect' ability, guarantee correct hint once
        if player.pop('next_hint', False):
            hint_is_correct = True
        else:
            hint_is_correct = random.random() < hint_prob
        hint = correct if hint_is_correct else ("left" if correct == "right" else "right")
        arrow = '<--' if hint == 'left' else '-->'
        delay_print(f"A gust of shards seems to come from the {hint.upper()} {arrow}")
        # run an ASCII dodge minigame: choose lane and watch projectiles fall
        avoided = animate_dodge_minigame(player, correct, attack_name=attack_name)
        if avoided:
            delay_print("You slip through the gap unscathed.")
            return
        else:
            dmg = random.randint(attack['min'], attack['max'])
            # apply shield if present
            if player.get('shield_turns', 0) > 0:
                dmg = max(0, dmg // 2)
                player['shield_turns'] -= 1
                delay_print("Your shield absorbs part of the blow.")
            player['hp'] -= dmg
            delay_print(f"You get hit for {dmg} damage.")
    else:
        # chance-based dodge: small probability to avoid
        dodge_chance = 0.35 if boss['phase'] == 1 else 0.4 if boss['phase'] == 3 else 0.3
        # acts and mood can slightly modify dodge difficulty
        dodge_chance += min(0.15, player.get('acts_done', 0) * 0.03)
        dodge_chance = min(0.7, dodge_chance)
        if random.random() < dodge_chance:
            delay_print("You manage to avoid the brunt of the attack.")
        else:
            dmg = random.randint(attack['min'], attack['max'])
            if player.get('shield_turns', 0) > 0:
                dmg = max(0, dmg // 2)
                player['shield_turns'] -= 1
                delay_print("Your shield absorbs part of the blow.")
            player['hp'] -= dmg
            delay_print(f"You take {dmg} damage.")


def environment_flavor(player, boss):
    lines = [
        "A distant drip echoes through the hollow.",
        "Dust motes swirl in a shaft of ghostly light.",
        "You hear an old bell toll somewhere far away.",
        "A faint warmth brushes your hand; then it's gone.",
    ]
    if random.random() < 0.25:
        delay_print(random.choice(lines), 0.4)


def check_phase(boss):
    if boss['hp'] <= 40 and boss['phase'] == 1:
        boss['phase'] = 2
        delay_print(f"{boss['name']} roars and shifts to Phase 2!")
    elif boss['hp'] <= 15 and boss['phase'] == 2:
        boss['phase'] = 3
        delay_print(f"{boss['name']} cracks and ignites a furious Phase 3!")


def animate_shards_preview(length=21, repeat=10, attack_name=None):
    """Simple left/right moving preview; symbol varies by attack."""
    symbol_map = {'shards': '*', 'spikes': '^', 'vine_laser': '~'}
    sym = symbol_map.get(attack_name, '*')
    speed = 0.07
    cycles = max(1, repeat // 2)
    for c in range(cycles):
        for pos in range(length):
            line = ' ' * pos + sym + ' ' * (length - pos - 1)
            print(line, end='\r')
            sys.stdout.flush()
            time.sleep(speed)
        for pos in range(length - 1, -1, -1):
            line = ' ' * pos + sym + ' ' * (length - pos - 1)
            print(line, end='\r')
            sys.stdout.flush()
            time.sleep(speed)
    print(' ' * length, end='\r')
    print()


def animate_onslaught_preview(phase, width=21, rows=3, frames=8, attack_name=None):
    """A quick multi-row flicker to simulate an onslaught; symbol varies by attack."""
    symbol_map = {'shards': '*', 'spikes': '^', 'vine_laser': '~'}
    sym = symbol_map.get(attack_name, '*')
    speed = 0.12
    for f in range(frames):
        for r in range(rows):
            line = [' ']*width
            # scatter some symbols; fewer for easier dodge
            for _ in range(1 + max(0, phase - 1)):
                idx = random.randrange(width)
                line[idx] = sym
            print(''.join(line))
        sys.stdout.flush()
        time.sleep(speed)
        # move cursor up `rows` lines to overwrite in next frame (ANSI)
        print(f"\x1b[{rows}A", end='')
    # clear the printed block
    print('\n' * rows)


def curses_dodge_minigame(correct_side, lanes=3, height=6):
    """Realtime dodge implemented with curses and arrow keys."""
    if curses is None:
        raise RuntimeError("curses not available")
    lane_names = ['left', 'center', 'right']

    def _run(stdscr):
        stdscr.nodelay(True)
        stdscr.keypad(True)
        try:
            curses.curs_set(0)
        except Exception:
            pass
        # prepare frames biased away from correct_side
        frames = []
        for f in range(height):
            choices = []
            for _ in range(1 + (f % 2)):
                if random.random() < 0.7:
                    if correct_side == 'left':
                        choices.append(random.choice(['center', 'right']))
                    else:
                        choices.append(random.choice(['left', 'center']))
                else:
                    choices.append(random.choice(lane_names))
            frames.append(choices)

        player_lane = 1
        for f_idx, proj in enumerate(frames):
            stdscr.clear()
            for row in range(height):
                parts = []
                for i, lane in enumerate(lane_names):
                    ch = ' '
                    if row == height - 1:
                        ch = 'A' if i == player_lane else ' '
                    else:
                        if row == f_idx and lane in proj:
                            ch = '*'
                    parts.append(ch)
                try:
                    stdscr.addstr(row, 0, ' | '.join(parts))
                except Exception:
                    pass

            stdscr.refresh()
            # wait with checking for arrow keys
            wait_end = time.time() + 0.16
            while time.time() < wait_end:
                k = stdscr.getch()
                if k == curses.KEY_LEFT:
                    player_lane = max(0, player_lane - 1)
                elif k == curses.KEY_RIGHT:
                    player_lane = min(lanes - 1, player_lane + 1)
                time.sleep(0.01)

        final_projectiles = frames[-1]
        hit = lane_names[player_lane] in final_projectiles
        return not hit

    return curses.wrapper(_run)


def animate_dodge_minigame(player, correct_side, attack_name=None, lanes=3, height=6):
    """Simple lane-based dodge minigame.

    Player chooses left/center/right. Projectiles fall down one of the lanes each frame.
    The `correct_side` is the safer side; projectiles are biased to the other side.
    Returns True if player avoided all projectiles, False if hit.
    """
    lane_names = ['left', 'center', 'right']
    # try curses arrow-key dodge first for richer control
    if curses is not None:
        try:
            return curses_dodge_minigame(correct_side, lanes=lanes, height=height)
        except Exception:
            pass
    # build frames: each frame is a set of lanes that have a projectile at that row
    frames = []
    # adjust spawn chance by attack type (make easier overall)
    spawn_base = 0.45
    if attack_name == 'spikes':
        spawn_base = 0.35
    elif attack_name == 'vine_laser':
        spawn_base = 0.4
    elif attack_name == 'shards':
        spawn_base = 0.3

    for f in range(height):
        choices = []
        if random.random() < spawn_base:
            # pick one lane to spawn (keep low density)
            if random.random() < 0.7:
                # bias away from correct side
                if correct_side == 'left':
                    choices.append(random.choice(['center', 'right']))
                else:
                    choices.append(random.choice(['left', 'center']))
            else:
                choices.append(random.choice(lane_names))
        frames.append(choices)

    # real-time mode: allow key presses (a/s/d) to move while projectiles fall
    delay_print("(Real-time) Use keys: 'a' = left, 's' = center, 'd' = right. Press Enter to start.", 0.01)
    try:
        input("Ready? ")
    except Exception:
        pass

    # Try to use immediate key reads on POSIX terminals; fallback to simple choice
    use_realtime = True
    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
    except Exception:
        use_realtime = False

    if not use_realtime:
        delay_print("Your terminal doesn't support realtime input; falling back.")
        choice = ask_choice("Dodge lane: ", lane_names)
        # simple frame render and final hit check
        for f_idx, proj in enumerate(frames):
            for row in range(height):
                line = []
                for lane in lane_names:
                    if row == height - 1:
                        line.append('A' if lane == choice else ' ')
                    else:
                        # choose symbol based on attack
                        sym = '^' if attack_name == 'spikes' else '~' if attack_name == 'vine_laser' else '*'
                        line.append(sym if row == f_idx and lane in proj else ' ')
                print(' | '.join(line))
            time.sleep(0.09)
            print(f"\x1b[{height}A", end='')
        final_projectiles = frames[-1]
        hit = choice in final_projectiles
        print('\n' * height)
        return not hit

    # realtime loop
    try:
        # use raw mode (disables echo and canonical mode) so keys don't print
        tty.setraw(sys.stdin.fileno())
        player_lane = 1  # start center (0=left,1=center,2=right)
        key_map = {'a': 0, 's': 1, 'd': 2}
        for f_idx, proj in enumerate(frames):
            # render frame with current player position
            for row in range(height):
                line = []
                for i, lane in enumerate(lane_names):
                    if row == height - 1:
                        line.append('A' if i == player_lane else ' ')
                    else:
                        sym = '^' if attack_name == 'spikes' else '~' if attack_name == 'vine_laser' else '*'
                        line.append(sym if row == f_idx and lane in proj else ' ')
                print(' | '.join(line))

            # small polling window for key presses while frame shows
            end = time.time() + 0.18
            while time.time() < end:
                dr, _, _ = select.select([sys.stdin], [], [], 0)
                if dr:
                    ch = sys.stdin.read(1)
                    if ch in key_map:
                        player_lane = key_map[ch]
                time.sleep(0.01)

            # move cursor up to redraw
            print(f"\x1b[{height}A", end='')

        final_projectiles = frames[-1]
        # collision if player's lane attacked in final frame
        hit = lane_names[player_lane] in final_projectiles
        print('\n' * height)
        return not hit
    finally:
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            pass


def boss_dialogue(boss, player):
    # pick base lines for the phase
    base = boss['dialogue'].get(boss['phase'], [])[:]
    extras = []
    # react to player's behavior
    if player.get('acts_done', 0) >= 3:
        extras.append("Your words... they linger.")
    if player.get('kills', 0) > 0:
        extras.append("Why spill so much?")
    if player.get('mercies', 0) > 0:
        extras.append("Mercy? You surprise me.")

    pool = base + extras
    if not pool:
        return
    line = random.choice(pool)
    # tone varies with mood
    tone = "(calm)" if boss.get('mood', 50) < 30 else "(irritated)" if boss.get('mood', 50) > 65 else "(measured)"
    delay_print(f"{boss['name']} {tone}: '{line}'", 0.9)


def ending(player, boss):
    if player['hp'] <= 0:
        delay_print("You fall... The hollow remains.")
        return
    # determine ending type
    if player['mercies'] > 0 and player['kills'] == 0:
        delay_print("Pacifist Ending: You spared the guardian and peace returns.")
    elif player['kills'] > 0 and player['mercies'] == 0:
        delay_print("Violent Ending: You defeated the guardian by force.")
    else:
        delay_print("Neutral Ending: The outcome is complicated; you live with the consequences.")


def play_expanded():
    header()
    player = make_player()
    boss = make_boss()

    boss_dialogue(boss, player)
    while player['hp'] > 0 and boss['hp'] > 0:
        show_status(player, boss)
        move = ask_choice("Choose (fight/act/item/mercy): ", ["fight", "act", "item", "mercy"])
        if move == 'fight':
            fight(player, boss)
            player['kills'] += 1
        elif move == 'act':
            act_menu(player, boss)
        elif move == 'item':
            item(player, boss)
        else:
            mercy(player, boss)

        if boss['hp'] <= 0:
            break

        check_phase(boss)
        boss_dialogue(boss, player)
        boss_attack(player, boss)

    ending(player, boss)


def main():
    while True:
        play_expanded()
        again = ask_choice("Play again? (yes/no): ", ["yes", "no"])
        if again == 'no':
            delay_print("Thanks for playing Understars Expanded!")
            break


if __name__ == '__main__':
    main()
