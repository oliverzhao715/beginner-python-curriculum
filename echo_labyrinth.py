import random
import time


def print_pause(message, delay=0.5):
    print(message)
    time.sleep(delay)


def get_choice(prompt, options):
    answer = input(prompt).strip().lower()
    while answer not in options:
        print(f"Choose one of: {', '.join(options)}")
        answer = input(prompt).strip().lower()
    return answer


def intro():
    print_pause("You enter the Echo Labyrinth.")
    print_pause("Every choice echoes back to you, and the wrong echo can trap you.")
    print_pause("Find the hidden exit before the echoes fade.")


def first_room(state):
    print_pause("Three paths stretch ahead: left, right, and straight.")
    choice = get_choice("Where do you go? left/right/straight: ", ["left", "right", "straight"])
    if choice == "left":
        print_pause("The walls hum softly. A whisper says: 'Seek the light.'")
        state['light_clue'] = True
        return "glow_room"
    if choice == "right":
        print_pause("The floor is cold and the air tastes like rain.")
        state['rain_clue'] = True
        return "mirror_room"
    print_pause("Straight ahead, the path narrows into darkness.")
    return "dark_room"


def glow_room(state):
    print_pause("A faint glow comes from a crystal in the corner.")
    action = get_choice("Do you inspect the crystal or continue? inspect/continue: ", ["inspect", "continue"])
    if action == "inspect":
        print_pause("The crystal shines and reveals a hidden door.")
        state['found_door'] = True
        return "exit_room"
    print_pause("You move past the crystal and it dims behind you.")
    return "dark_room"


def mirror_room(state):
    print_pause("The walls are mirrors. Your reflection stares before you.")
    action = get_choice("Do you speak to your reflection or turn away? speak/away: ", ["speak", "away"])
    if action == "speak":
        print_pause("Your reflection says: 'The exit hides where the light is shy.'")
        state['light_clue'] = True
        return "glow_room"
    print_pause("You turn away and find a narrow stair down.")
    return "pit_room"


def dark_room(state):
    print_pause("The darkness presses close. You hear the echo of your own heart.")
    action = get_choice("Do you light a match or wait? match/wait: ", ["match", "wait"])
    if action == "match":
        if state.get('light_clue'):
            print_pause("The match reveals a hidden path and a bright exit beyond.")
            return "exit_room"
        print_pause("The light flickers, but the path vanishes. You remain lost.")
        return "pit_room"
    print_pause("The echoes grow louder and a voice whispers: 'the path is not the sound.'")
    return "mirror_room"


def pit_room(state):
    print_pause("A pit blocks the path. The echo of a breeze comes from the left.")
    action = get_choice("Do you jump left or right? left/right: ", ["left", "right"])
    if action == "left" and state.get('rain_clue'):
        print_pause("The breeze was a warning. You land safely and see a glowing exit.")
        return "exit_room"
    if action == "right":
        print_pause("You fall into a shallow hole but climb out, shaken.")
        return "dark_room"
    print_pause("You can't find stable footing and the echo fades.")
    return "mirror_room"


def exit_room(state):
    print_pause("You stand before the exit. The final door is sealed by a riddle.")
    riddle = "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?"
    print_pause(riddle)
    answer = input("Answer: ").strip().lower()
    if answer == "echo":
        print_pause("The door opens with a warm sound. You escape the labyrinth.")
        state['escaped'] = True
    else:
        print_pause("The door remains closed. The echo is not satisfied.")
        state['escaped'] = False
    return "end"


def play_labyrinth():
    intro()
    state = {"escaped": False}
    room = "first"
    steps = 0
    while room != "end" and steps < 8:
        if room == "first":
            room = first_room(state)
        elif room == "glow_room":
            room = glow_room(state)
        elif room == "mirror_room":
            room = mirror_room(state)
        elif room == "dark_room":
            room = dark_room(state)
        elif room == "pit_room":
            room = pit_room(state)
        elif room == "exit_room":
            room = exit_room(state)
        steps += 1
    if state.get('escaped'):
        print_pause("You escaped with your wits and the echoes as your guide.")
    else:
        print_pause("The labyrinth closes around you. Try again to find the right echoes.")


def main():
    while True:
        play_labyrinth()
        again = get_choice("Play again? (yes/no): ", ["yes", "no"])
        if again == "no":
            print_pause("Thanks for exploring the Echo Labyrinth!")
            break


if __name__ == "__main__":
    main()
