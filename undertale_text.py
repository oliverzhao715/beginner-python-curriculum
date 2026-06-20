#!/usr/bin/env python3
"""
UNDERTALE-LIKE TEXT ADVENTURE — The Hollow Guardian
Terminal-based, dialogue-heavy, multiple phases with personality shifts.
Run: python3 undertale_text.py
"""

import time
import random
import sys

# ============================================================================
# DIALOGUE LIBRARY — Phase-dependent personalities & responses
# ============================================================================

DIALOGUES = {
    "phase1_idle": [
        "Guardian: ...",
        "Guardian: Hello there. I suppose you've come to test your strength?",
        "Guardian: How... quaint.",
        "Guardian: *watches you with a single luminous eye*",
        "Guardian: You know, not many reach this deep. I'm almost impressed.",
        "Guardian: Also, this chamber could use better lighting. Ever heard of candles?",
        "Guardian: If you brought snacks, now would be a great time to share.",
    ],
    "phase1_taunts": [
        "Guardian: That was... pathetic.",
        "Guardian: Is that really all you've got? How disappointing.",
        "Guardian: You're brave. Or stupid. Probably stupid.",
        "Guardian: Did you really think that would work?",
        "Guardian: I'm barely awake right now. You might want to try harder.",
        "Guardian: Even my cactus could sidestep that move.",
        "Guardian: I've seen better attacks from a sleepy goldfish.",
    ],
    "phase1_hurt": [
        "Guardian: Oh... you actually landed a hit.",
        "Guardian: Okay, okay. I see you.",
        "Guardian: Alright, I'm starting to take you seriously now.",
        "Guardian: Not bad. For a mortal.",
        "Guardian: That tickled. In a dangerous way.",
    ],
    "phase2_idle": [
        "Guardian: ...You're still here?",
        "Guardian: Fine. FINE. Let's get SERIOUS then.",
        "Guardian: You want a real fight? You've got it now.",
        "Guardian: * The guardian's eye GLOWS brighter *",
        "Guardian: I was being NICE. That's over.",
        "Guardian: Also, if you were a sandwich, you'd be a soggy one.",
    ],
    "phase2_taunts": [
        "Guardian: You think you're clever?! You're NOTHING!",
        "Guardian: I'm just getting started, you little pest!",
        "Guardian: You dare damage me?! I'll crush you!",
        "Guardian: Stop wasting my TIME!",
        "Guardian: Your attacks are PATHETIC! TRY HARDER!",
    ],
    "phase2_hurt": [
        "Guardian: THAT HURT! YOU MADE ME ACTUALLY ANGRY!",
        "Guardian: Oh, you want to play DIRTY now?",
        "Guardian: *The air around the guardian crackles with energy*",
        "Guardian: You're going to PAY for that!",
    ],
    "phase3_idle": [
        "Guardian: ENOUGH GAMES! ENOUGH!",
        "Guardian: I'VE HAD IT WITH YOU!",
        "Guardian: YOU THINK YOU'RE STRONG?! YOU THINK YOU CAN BEAT ME?!",
        "Guardian: * The guardian EXPLODES with blinding light *",
        "Guardian: I WILL ERASE YOU FROM EXISTENCE!",
    ],
    "phase3_taunts": [
        "Guardian: DIE! DIE! DIE!!!",
        "Guardian: I'LL RIP YOU APART!",
        "Guardian: YOUR HOPE MEANS NOTHING TO ME!",
        "Guardian: SURRENDER NOW AND I MIGHT MAKE IT QUICK!",
        "Guardian: THERE'S NO ESCAPE! NOWHERE TO RUN!",
        "Guardian: And if I win, I'm putting \"You lost\" on a T-shirt.",
    ],
    "phase3_hurt": [
        "Guardian: NO! NO NO NO! THIS CAN'T BE!",
        "Guardian: HOW ARE YOU STILL STANDING?!",
        "Guardian: I... I CAN'T LOSE TO YOU!",
        "Guardian: *The guardian's form flickers and distorts*",
        "Guardian: THIS ISN'T OVER! NOT YET!",
    ],
    "act1": [
        "You observe the guardian.",
        "It's an old, powerful entity. Its single eye is ancient and tired.",
        "Strangely, it seems... lonely.",
    ],
    "act2": [
        "You try to understand the guardian.",
        "Flashes of memory appear: endless years of isolation.",
        "Watching. Always watching. Never letting anyone pass.",
    ],
    "act3": [
        "You reach out to the guardian.",
        "For a moment, something shifts in its eye.",
        "The glow dims ever so slightly...",
    ],
    "chat_phase1": [
        "Guardian: Hello? Who is talking to me?",
        "Guardian: If you're planning on fighting later, at least say it clearly.",
        "Guardian: You humans are always so loud. Do you mind?",
    ],
    "chat_phase2": [
        "Guardian: Great, another mouth to answer.",
        "Guardian: I don't usually chat during battles. This is new.",
        "Guardian: You're persistent. I'll give you that.",
    ],
    "chat_phase3": [
        "Guardian: Talk all you want. It won't save you.",
        "Guardian: Your words are distractions. Focus or leave.",
        "Guardian: Hah. If words were weapons, you'd have an army.",
    ],
    "chat_friendly": [
        "Guardian: Fine. I suppose conversation isn't the worst way to pass the time.",
        "Guardian: You talk a lot for someone about to die.",
        "Guardian: I guess you do have a strange charm.",
    ],
    "chat_insult": [
        "Guardian: Save your breath, your threats are adorable.",
        "Guardian: I have faced storms stronger than your insults.",
        "Guardian: You're trying to be scary? Cute.",
    ],
    "chat_mercy": [
        "Guardian: Mercy? Why would I accept mercy from you?",
        "Guardian: Hmm. That's surprisingly civilized.",
        "Guardian: If I spare you, will you stop talking?",
    ],
    "chat_joke": [
        "Guardian: Haha. I did not expect a joke in the middle of a fight.",
        "Guardian: You should be a comedian. Preferably a dead one.",
        "Guardian: That was almost amusing. Almost.",
    ],
    "mercy_turn": [
        "Guardian: ...",
        "Guardian: Why would you show mercy to something like me?",
        "Guardian: Do you truly believe I can change?",
    ],
    "mercy_win": [
        "",
        "* The guardian's form begins to dissolve *",
        "",
        "Guardian: I... I remember now.",
        "Guardian: There was a time before this. Before the endless guarding.",
        "Guardian: I was... lonely. So very lonely.",
        "",
        "Guardian: Thank you.",
        "Guardian: ...Go. Leave this place. Live the life I never could.",
        "",
        "* The guardian fades into particles of light *",
        "",
        "*** TRUE PACIFIST ENDING ***",
        "You've freed the guardian from its eternal prison.",
    ],
    "fight_win": [
        "",
        "* The guardian's light falters and dims *",
        "",
        "Guardian: I... I've been defeated.",
        "Guardian: After so long... how is this possible...",
        "",
        "* The guardian collapses *",
        "",
        "Guardian: You were strong. Stronger than anyone before.",
        "Guardian: Perhaps I was wrong about everything.",
        "",
        "*** NEUTRAL ENDING ***",
        "You've conquered the guardian.",
    ],
    "game_over": [
        "",
        "* Your vision fades *",
        "",
        "Guardian: This is what happens when you challenge something beyond your comprehension.",
        "Guardian: Rest now. Your journey ends here.",
        "",
        "*** GAME OVER ***",
        "The guardian stands victorious.",
    ],
}

ACT_DESCRIPTIONS = {
    "phase1": {
        "act1": "Observe the guardian",
        "act2": "Study its movements",
        "act3": "Reach out gently",
    },
    "phase2": {
        "act1": "Mock the guardian",
        "act2": "Challenge its strength",
        "act3": "Appeal to its past",
    },
    "phase3": {
        "act1": "Taunt back fiercely",
        "act2": "Match its aggression",
        "act3": "Show your resolve",
    },
}

# ============================================================================
# GAME STATE & UTILITIES
# ============================================================================

def slow_print(text, delay=0.02):
    """Print text with typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def pause(duration=0.8):
    """Brief pause for pacing."""
    time.sleep(duration)

def show_separator():
    """Print a separator line."""
    print("\n" + "=" * 70 + "\n")

def get_input(prompt):
    """Get user input with retry logic."""
    while True:
        try:
            choice = input(prompt).strip().lower()
            if choice:
                return choice
        except EOFError:
            return "fight"  # default if piped
        except KeyboardInterrupt:
            print("\n\n[You flee in terror!]")
            sys.exit(0)

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class Player:
    def __init__(self):
        self.hp = 20
        self.max_hp = 20
        self.attack_power = 3
        self.defense = 1
        
    def take_damage(self, dmg):
        reduced = max(1, dmg - self.defense)
        self.hp -= reduced
        return reduced

class Guardian:
    def __init__(self):
        self.name = "The Hollow Guardian"
        self.hp = 50
        self.max_hp = 50
        self.phase = 1
        self.dodge_chance = 0.12
        self.last_action = None
        self.chat_affinity = 0
        self.peaceful = False
        self.chat_history = []
        
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= self.max_hp * 0.65 and self.phase == 1:
            self.phase = 2
            self.dodge_chance = 0.22
        elif self.hp <= self.max_hp * 0.3 and self.phase == 2:
            self.phase = 3
            self.dodge_chance = 0.32
        return dmg
        
    def attack(self):
        """Boss attacks with phase-appropriate damage & behavior."""
        if self.phase == 1:
            dmg = random.randint(2, 4)
        elif self.phase == 2:
            dmg = random.randint(4, 7)
        else:  # phase 3
            dmg = random.randint(6, 10)
        return dmg

def show_status(player, boss):
    """Display HP bars and phase info."""
    print(f"\n[{boss.name} — Phase {boss.phase}]")
    
    # Boss HP
    bar_length = 30
    filled = int((boss.hp / boss.max_hp) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"Boss HP: [{bar}] {boss.hp}/{boss.max_hp}")
    
    # Player HP
    filled = int((player.hp / player.max_hp) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"Your HP: [{bar}] {player.hp}/{player.max_hp}\n")

def show_menu():
    """Display the action menu."""
    print("[1] FIGHT  [2] ACT  [3] ITEM  [4] MERCY  [5] CHAT")
    return get_input("> ").lower()

# ============================================================================
# ACTION HANDLERS
# ============================================================================

def action_fight(player, boss):
    """Player attacks."""
    print()
    
    # Dialogue before attack
    if random.random() < 0.6:
        slow_print(f"You prepare to strike the guardian!")
    
    pause()
    
    # Calculate damage
    base_dmg = player.attack_power + random.randint(-1, 3)
    
    # Boss dodge check
    if random.random() < boss.dodge_chance:
        print("\n>>> The guardian DODGES your attack! <<<")
        slow_print(DIALOGUES["phase" + str(boss.phase) + "_taunts"][0])
        boss.last_action = "dodge"
        return False
    
    # Hit lands
    actual_dmg = boss.take_damage(base_dmg)
    print(f"\n>>> You deal {actual_dmg} damage! <<<")
    
    # Reaction dialogue
    if boss.hp > 0:
        if boss.phase == 1 and boss.hp <= boss.max_hp * 0.65 and boss.phase == 1:
            # Phase transition
            print()
            slow_print("Guardian: Oh. OH. You actually hurt me.")
            slow_print("Guardian: I see. You're not just stumbling blindly then.")
            slow_print("Guardian: ...Fine. No more holding back.")
        elif boss.phase == 2 and boss.hp <= boss.max_hp * 0.3 and boss.phase == 2:
            # Second phase transition
            print()
            slow_print("Guardian: IMPOSSIBLE! YOU'RE PUSHING ME BACK?!")
            slow_print("Guardian: FINE! IF THAT'S HOW YOU WANT IT!")
            slow_print("Guardian: I HAVE SLEPT FOR AGES. I HAVE FORGOTTEN MY FURY.")
            slow_print("Guardian: LET ME REMIND MYSELF!")
        elif random.random() < 0.5:
            slow_print(random.choice(DIALOGUES["phase" + str(boss.phase) + "_hurt"]))
    
    boss.last_action = "hit"
    return True

def action_act(player, boss):
    """ACT menu — personality changes per phase."""
    print("\n--- WHAT DO YOU DO? ---")
    
    acts = ACT_DESCRIPTIONS[f"phase{boss.phase}"]
    print(f"[1] {acts['act1']}")
    print(f"[2] {acts['act2']}")
    print(f"[3] {acts['act3']}")
    print(f"[4] Back")
    
    choice = get_input("> ").lower()
    
    if choice == "1":
        print()
        slow_print(random.choice(DIALOGUES["act1"]))
    elif choice == "2":
        print()
        slow_print(random.choice(DIALOGUES["act2"]))
    elif choice == "3":
        print()
        slow_print(random.choice(DIALOGUES["act3"]))
    elif choice == "4":
        return action_act(player, boss)  # Recurse back to menu (or just return)
    
    pause(1.2)
    print()
    
    # Boss reaction varies by phase
    if boss.phase == 1:
        slow_print("Guardian: Interesting approach. Still won't save you.")
    elif boss.phase == 2:
        slow_print("Guardian: STOP TOYING WITH ME! JUST FIGHT LIKE A WARRIOR!")
    else:
        slow_print("Guardian: YOUR PATHETIC WORDS MEAN NOTHING! FACE ME!")
    
    if boss.phase == 1 and random.random() < 0.4:
        slow_print("Guardian: Also, your fashion sense is... ambitious.")
    elif boss.phase == 2 and random.random() < 0.3:
        slow_print("Guardian: You have the emotional range of a soggy crouton.")
    elif boss.phase == 3 and random.random() < 0.2:
        slow_print("Guardian: Tell me your secrets later. Or don't. I don't care.")
    
    if boss.phase == 1 and random.random() < 0.3:
        slow_print("Guardian: If you had a theme song, it would be 'questionably competent.'")
    elif boss.phase == 2 and random.random() < 0.25:
        slow_print("Guardian: By the way, your overlord called. He wants his hesitation back.")
    elif boss.phase == 3 and random.random() < 0.15:
        slow_print("Guardian: Seriously, stop narrating your strategy out loud.")
    
    return False  # ACT doesn't damage

def action_item(player, boss):
    """Use an item."""
    print("\n--- ITEMS ---")
    
    heal_amount = 5
    old_hp = player.hp
    player.hp = min(player.max_hp, player.hp + heal_amount)
    actual_heal = player.hp - old_hp
    
    print()
    slow_print(f"You drink a potion and recover {actual_heal} HP.")
    pause(0.8)
    
    if boss.phase == 1:
        slow_print("Guardian: Running away to heal? Smart. But it won't help.")
        slow_print("Guardian: Also, your potion smells suspiciously like berry juice.")
    elif boss.phase == 2:
        slow_print("Guardian: COWARD! HIDING BEHIND YOUR ITEMS?!")
        slow_print("Guardian: If that potion came with a coupon, I'll take it.")
    else:
        slow_print("Guardian: PATHETIC! YOUR POTIONS CAN'T SAVE YOU NOW!")
        slow_print("Guardian: But hey, at least your inventory looks organized.")
    
    return False  # ITEM doesn't attack

def generate_ai_response(message, boss):
    """Generate a simple AI-style response for the guardian."""
    msg = message.lower()
    boss.chat_history.append(message)
    peaceful_phrases = [
        "i don't want to fight",
        "i dont want to fight",
        "i do not want to fight",
        "please don't fight",
        "please do not fight",
        "i don't want to hurt you",
        "i dont even wanna fight",
        "i dont want to hurt you",
        "don't fight",
        "do not fight",
        "let's not fight",
        "i just want peace",
        "peace",
    ]
    if any(phrase in msg for phrase in peaceful_phrases):
        boss.peaceful = True
        return ("Guardian: ...You don't want to fight? That's surprisingly honest.", 3)
    if any(word in msg for word in ["mercy", "spare", "please", "live"]):
        return ("Guardian: Mercy again? Maybe I'm impressed by your persistence.", 2)
    if any(word in msg for word in ["hello", "hi", "hey"]):
        return (random.choice(DIALOGUES[f"chat_phase{boss.phase}"]), 0)
    if any(word in msg for word in ["joke", "lol", "haha", "funny"]):
        return (random.choice(DIALOGUES["chat_joke"]), 1)
    if any(word in msg for word in ["stupid", "idiot", "dumb", "ugly"]):
        return (random.choice(DIALOGUES["chat_insult"]), -1)
    if "why" in msg:
        return ("Guardian: Because I was made to guard. That's what I do.", 0)
    if "who are you" in msg or "who are you?" in msg:
        return ("Guardian: I am the Hollow Guardian. You are the intruder.", 0)
    if "help" in msg:
        return ("Guardian: I am not your guide. I am your challenge.", 0)
    if msg.endswith("?"):
        return ("Guardian: That's an interesting question. I will answer it if worthy.", 0)
    if len(msg.split()) <= 2:
        return ("Guardian: Short words. Big danger.", 0)
    return ("Guardian: Your words are curious. I have not heard that phrasing before.", 0)

def action_chat(player, boss):
    """Chat with the guardian using free-form typed text."""
    print("\n--- CHAT ---")
    slow_print("Type what you want to say. Example: 'I don't want to fight you.'")
    message = get_input("> ")
    response, delta = generate_ai_response(message, boss)
    boss.chat_affinity += delta
    slow_print(response)
    
    if boss.chat_affinity >= 3:
        slow_print("Guardian: You know what? You're actually kind of interesting.")
    elif boss.chat_affinity <= -2:
        slow_print("Guardian: Fine. If you insist on being rude, I'll be ruthless.")
    
    pause(1.2)
    return

def action_mercy(player, boss):
    """Attempt MERCY — only works if boss is convinced."""
    print()
    
    # Mercy effectiveness based on dialogue choices & phase
    if boss.phase == 1:
        mercy_chance = 0.3  # Hard to convince at first
    elif boss.phase == 2:
        mercy_chance = 0.4  # Getting there
    else:
        mercy_chance = 0.5  # If you're still here in phase 3...
    
    slow_print("You extend your hand in peace...")
    pause(1.2)
    
    # Mercy becomes easier with a friendlier connection.
    mercy_chance += min(0.2, boss.chat_affinity * 0.05)
    if random.random() < mercy_chance:
        print()
        slow_print(random.choice(DIALOGUES["mercy_turn"]))
        return "pacifist"
    else:
        print()
        slow_print("Guardian: Nice try. Your mercy means nothing to me.")
        slow_print("Guardian: But I do appreciate the effort. That was adorable.")
        return False

# ============================================================================
# MAIN BATTLE LOOP
# ============================================================================

def play_battle():
    """Main game loop."""
    player = Player()
    boss = Guardian()
    
    # Intro
    show_separator()
    slow_print("You step into a vast, ancient chamber.")
    pause(1.5)
    slow_print("A single luminous eye opens in the darkness...")
    pause(1.5)
    print()
    slow_print(random.choice(DIALOGUES["phase1_idle"]))
    pause(1.5)
    
    show_separator()
    
    turn = 0
    while True:
        turn += 1
        show_status(player, boss)
        
        # Player turn
        print(f"--- TURN {turn} ---")
        action = show_menu()
        
        if action == "1":
            action_fight(player, boss)
        elif action == "2":
            action_act(player, boss)
        elif action == "3":
            action_item(player, boss)
        elif action == "4":
            result = action_mercy(player, boss)
            if result == "pacifist":
                show_separator()
                for line in DIALOGUES["mercy_win"]:
                    slow_print(line)
                    pause(0.5)
                return
        elif action == "5":
            action_chat(player, boss)
        else:
            slow_print("Guardian: Make a choice already!")
            continue
        
        # Check if boss is defeated
        if boss.hp <= 0:
            show_separator()
            for line in DIALOGUES["fight_win"]:
                slow_print(line)
                pause(0.5)
            return
        
        show_separator()
        
        # Boss turn
        print("[Boss's Turn]")
        dmg = boss.attack()
        
        if boss.phase == 1:
            slow_print(random.choice(DIALOGUES["phase1_taunts"]))
        elif boss.phase == 2:
            slow_print(random.choice(DIALOGUES["phase2_taunts"]))
        else:
            slow_print(random.choice(DIALOGUES["phase3_taunts"]))
        
        pause(0.8)
        if boss.peaceful and boss.chat_affinity >= 2:
            slow_print("Guardian: ...Fine. I'll hold my strike this turn. Don't waste it.")
            boss.peaceful = False
        else:
            reduced_dmg = player.take_damage(dmg)
            print(f"\n>>> You take {reduced_dmg} damage! <<<")
        pause(0.8)
        
        # Check if player is defeated
        if player.hp <= 0:
            show_separator()
            for line in DIALOGUES["game_over"]:
                slow_print(line)
                pause(0.5)
            return
        
        show_separator()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    try:
        play_battle()
        print("\n[Thanks for playing!]\n")
    except KeyboardInterrupt:
        print("\n\n[You flee into the darkness...]\n")
        sys.exit(0)
