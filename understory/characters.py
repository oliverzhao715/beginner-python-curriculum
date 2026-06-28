class Character:
    def __init__(self, name, hp, attack=1, mercy=0):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.mercy = mercy

    def is_alive(self):
        return self.hp > 0


class Player(Character):
    def __init__(self, name="Player", hp=20, attack=3):
        super().__init__(name, hp, attack, mercy=0)
        self.items = {"potion": 2}


class Enemy(Character):
    def __init__(self, name, hp=10, attack=2, mercy=1):
        super().__init__(name, hp, attack, mercy)
