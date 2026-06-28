import random


class GameEngine:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 0

    def start_battle(self):
        print("\n--- Battle Start ---\n")
        while self.player.is_alive() and self.enemy.is_alive():
            self.turn += 1
            self.display_status()
            self.player_turn()
            if not self.enemy.is_alive():
                print(f"{self.enemy.name} spared! You win the encounter." )
                break
            self.enemy_turn()
        if not self.player.is_alive():
            print("You fainted. Game over.")

    def display_status(self):
        print(f"{self.player.name}: {self.player.hp}/{self.player.max_hp} HP")
        print(f"{self.enemy.name}: {self.enemy.hp}/{self.enemy.max_hp} HP\n")

    def player_turn(self):
        action = self.prompt_action()
        if action == "fight":
            dmg = max(0, self.player.attack + random.randint(-1, 2))
            self.enemy.hp -= dmg
            print(f"You attack and deal {dmg} damage.")
        elif action == "act":
            self.act_menu()
        elif action == "item":
            self.use_item()
        elif action == "mercy":
            if self.attempt_mercy():
                self.enemy.hp = 0
            else:
                print("Mercy failed.")

    def prompt_action(self):
        choices = ["fight", "act", "item", "mercy"]
        while True:
            choice = input("Choose an action [fight/act/item/mercy]: ").strip().lower()
            if choice in choices:
                return choice
            print("Invalid action. Try again.")

    def act_menu(self):
        print("You try to understand the enemy.")
        # small fiction: reduce enemy aggression
        self.enemy.attack = max(0, self.enemy.attack - 1)
        print(f"{self.enemy.name} seems calmer.")

    def use_item(self):
        if self.player.items.get("potion", 0) > 0:
            self.player.items["potion"] -= 1
            heal = 8
            self.player.hp = min(self.player.max_hp, self.player.hp + heal)
            print(f"You use a potion and heal {heal} HP.")
        else:
            print("No items left.")

    def attempt_mercy(self):
        # mercy depends on enemy mercy stat and how calm they are (lower attack)
        chance = 0.2 + 0.15 * (self.enemy.mercy) - 0.05 * (self.enemy.attack)
        roll = random.random()
        print(f"Mercy roll: {roll:.2f} <= {chance:.2f}")
        return roll <= max(0.05, chance)

    def enemy_turn(self):
        dmg = max(0, self.enemy.attack + random.randint(-1, 1))
        self.player.hp -= dmg
        print(f"{self.enemy.name} attacks and deals {dmg} damage.\n")
