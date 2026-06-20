#!/usr/bin/env python3
"""
RAGEBAIT — A tiny collection of deliberately annoying, non-violent terminal mini-games.
Run: python3 ragebait.py
"""

import random
import sys
import time

TAUNTS = [
    "Are you sure you want to be this committed to frustration?",
    "So close. So far.",
    "You asked for this.",
    "Patience is a virtue. You're not virtuous.",
    "Who's laughing now? Not you.",
]

# --- utilities

def slow_print(s, delay=0.01):
    for ch in s:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def prompt(msg):
    return input(msg + " \n> ").strip()

# --- mini-games

def button_roulette(rounds=5):
    """Prompt to press a shown key, but mapping shuffles each time."""
    print("\n== Button Roulette ==")
    score = 0
    keys = list('asdfjkl;')
    for r in range(1, rounds+1):
        target = random.choice(keys)
        mapping = keys[:]
        random.shuffle(mapping)
        print(f"Round {r}: Press '{target}'")
        print("Key mapping (annoyingly shuffled):")
        print(' '.join(mapping))
        ans = prompt("Press the key you think is the target (type it).")
        if ans == target:
            print("Nice. You matched it. For now.")
            score += 1
        elif ans in mapping:
            print("Close, but the universe had other plans.")
        else:
            print(random.choice(TAUNTS))
        # sometimes shuffle keys mid-round
        if random.random() < 0.25:
            print("Oh no—the keyboard remapped itself!")
            random.shuffle(mapping)
        time.sleep(0.6)
    print(f"Button Roulette score: {score}/{rounds}")
    return score


def fake_progress_bar(length=30):
    """Show a fake progress bar that resets a few times unless you answer a riddle."""
    print("\n== Progress Troll ==")
    print("Watch the progress bar carefully. Or don't.")
    for attempt in range(1,4):
        for i in range(length+1):
            pct = int((i/length)*100)
            bar = '#' * i + '-' * (length-i)
            sys.stdout.write(f"\r[{bar}] {pct}%")
            sys.stdout.flush()
            time.sleep(0.03 + random.random()*0.03)
        time.sleep(0.2)
        if attempt < 3 and random.random() < 0.8:
            print('\n...oops! progress corrupted. restarting...')
            time.sleep(0.7)
        else:
            print('\nDone? Not quite.')
    print("Answer a tiny riddle to actually finish: What has keys but no locks?")
    ans = prompt("Type your answer")
    if 'piano' in ans.lower() or 'keyboard' in ans.lower():
        slow_print("Fine. The progress is real. You're welcome.")
        return True
    else:
        slow_print("Wrong. The progress remains imaginary.")
        return False


def trap_words(rounds=6):
    """Type words quickly; some words are traps that scramble your input temporarily."""
    print("\n== Trap Words ==")
    words = ["apple","dragon","mirror","honor","ghost","puzzle","banana","light"]
    score = 0
    for r in range(rounds):
        w = random.choice(words)
        trap = random.random() < 0.35
        print(f"Type this word: {w}")
        if trap:
            print("(Warning: trap word — your input may be scrambled briefly)")
        ans = prompt("type it now")
        if trap and random.random() < 0.6:
            # invert input, swap letters
            scrambled = ''.join(reversed(ans))
            print(f"Your input mutated into: {scrambled}")
            if scrambled == w:
                print("Lucky mutation! You win this one.")
                score += 1
            else:
                print("Nope. The trap had its way.")
        else:
            if ans == w:
                print("Correct. For now.")
                score += 1
            else:
                print(random.choice(TAUNTS))
        time.sleep(0.4)
    print(f"Trap Words score: {score}/{rounds}")
    return score


def almost_perfect_timing(rounds=5):
    """Ask user to press Enter within a tightening window."""
    print("\n== Almost-Perfect Timing ==")
    print("Press Enter when the countdown hits 0. Windows shrink each round.")
    score = 0
    base = 1.2
    for r in range(rounds):
        wait = base - r * 0.18
        print("Get ready...")
        time.sleep(1.0 + random.random()*0.6)
        sys.stdout.write("3...")
        sys.stdout.flush(); time.sleep(0.4)
        sys.stdout.write("2...")
        sys.stdout.flush(); time.sleep(0.4)
        sys.stdout.write("1...")
        sys.stdout.flush(); time.sleep(0.4)
        print("0! Press Enter NOW!")
        start = time.time()
        input()
        elapsed = time.time() - start
        # success if within window; window is small
        if elapsed <= wait:
            print("Perfect! You beat the shrinking window.")
            score += 1
        else:
            print(f"Too slow (you took {elapsed:.2f}s).")
        time.sleep(0.3)
    print(f"Timing score: {score}/{rounds}")
    return score

# --- extra annoying games
def eternal_progress_bar(length=80):
    """Longer, nastier fake progress that rarely finishes."""
    print("\n== Eternal Progress Troll ==")
    for attempt in range(1,6):
        for i in range(length+1):
            pct = int((i/length)*100)
            bar = '#' * i + '-' * (length-i)
            sys.stdout.write(f"\r[{bar}] {pct}%")
            sys.stdout.flush()
            time.sleep(0.02 + random.random()*0.04)
        print('\nSystem glitch: rollback initiated...')
        time.sleep(0.6)
        if attempt == 5:
            print('\nA mysterious admin appears and demands a riddle.')
            ans = prompt('What has a ring but no finger?')
            if 'telephone' in ans.lower() or 'phone' in ans.lower():
                slow_print('The admin is satisfied. Progress completes.')
                return True
            else:
                slow_print('Wrong. Eternal rollback continues.')
                return False

def mimic_typo(rounds=5):
    """Type a shown word; program randomly mutates target and input may be judged harshly."""
    print("\n== Mimic Typo ==")
    words = ['courage','fortune','pillow','mystery','cobalt','flannel']
    score = 0
    for _ in range(rounds):
        w = random.choice(words)
        print(f"Type this exactly: {w}")
        ans = prompt('> ')
        # mutate expected occasionally
        if random.random() < 0.5:
            mutated = list(w)
            i = random.randrange(len(mutated))
            mutated[i] = random.choice('abcdefghijklmnopqrstuvwxyz')
            w2 = ''.join(mutated)
            print(f"(System mutated target to: {w2})")
            if ans == w2:
                print('Weird, you matched the mutated target. +1')
                score += 1
            else:
                print(random.choice(TAUNTS))
        else:
            if ans == w:
                print('Correct, but not for long.')
                score += 1
            else:
                print('Nope.')
    print(f"Mimic Typo score: {score}/{rounds}")
    return score

def whack_letter(rounds=6):
    """Press the shown letter; mapping sometimes flips to annoy you."""
    print("\n== Whack-a-Letter ==")
    letters = list('qwertyuiop')
    score = 0
    for r in range(rounds):
        L = random.choice(letters)
        flipped = random.random() < 0.35
        if flipped:
            print(f"Quick! Press '{L}' (but keyboard is flipped!)")
            ans = prompt('> ')
            # simulate flip by reversing the ans
            if ans[::-1] == L:
                print('You managed the flip. Bravo.')
                score += 1
            else:
                print('That did not go as planned.')
        else:
            print(f"Quick! Press '{L}'")
            ans = prompt('> ')
            if ans == L:
                print('Good reflexes.')
                score += 1
            else:
                print(random.choice(TAUNTS))
    print(f"Whack-a-Letter score: {score}/{rounds}")
    return score

def simon_shuffle(rounds=4):
    """Memory sequence where symbols remap each round."""
    print("\n== Simon Shuffle ==")
    symbols = ['A','B','C','D']
    mapping = symbols[:]
    score = 0
    seq = []
    for r in range(rounds):
        seq.append(random.choice(symbols))
        random.shuffle(mapping)
        print('Sequence to remember:', ' '.join(seq))
        ans = prompt('Repeat the sequence (space separated)').upper()
        if ans == ' '.join(seq):
            print('Correct, for now.')
            score += 1
        else:
            print('Nope. Sequence was lost in static.')
    print(f"Simon Shuffle score: {score}/{rounds}")
    return score

# --- main flow

def main():
    slow_print("RAGEBAIT — Nonviolent Annoyance Suite", 0.02)
    slow_print("Pick a mode. These are purposely frustrating. Don't say I didn't warn you.")
    total = 0
    while True:
        print("\nModes: [1] Button Roulette  [2] Progress Troll  [3] Trap Words  [4] Timing  [5] Random Mashup")
        print("       [6] Eternal Progress  [7] Mimic Typo  [8] Whack-a-Letter  [9] Simon Shuffle  [q] Quit")
        choice = prompt("Choose a mode")
        if choice == '1':
            total += button_roulette()
        elif choice == '2':
            ok = fake_progress_bar()
            total += 1 if ok else 0
        elif choice == '3':
            total += trap_words()
        elif choice == '4':
            total += almost_perfect_timing()
        elif choice == '5':
            # quick random mashup
            funcs = [button_roulette, fake_progress_bar, trap_words, almost_perfect_timing]
            f = random.choice(funcs)
            total += (f() if f is not fake_progress_bar else (1 if fake_progress_bar() else 0))
        elif choice == '6':
            total += 1 if eternal_progress_bar() else 0
        elif choice == '7':
            total += mimic_typo()
        elif choice == '8':
            total += whack_letter()
        elif choice == '9':
            total += simon_shuffle()
        elif choice.lower() == 'q':
            slow_print(f"You quit. Total 'wins' counted: {total}")
            break
        else:
            print("Please select a valid mode.")
        # occasional taunt
        if random.random() < 0.45:
            print("\n" + random.choice(TAUNTS) + "\n")
    slow_print("Thanks for playing. You have been successfully annoyed.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
