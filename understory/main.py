from engine import GameEngine
from characters import Player, Enemy


def main():
    player = Player(name="You")
    enemy = Enemy(name="Mosskin", hp=18, attack=4, mercy=2)
    engine = GameEngine(player, enemy)
    engine.start_battle()


if __name__ == "__main__":
    main()
