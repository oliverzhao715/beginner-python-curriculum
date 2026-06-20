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
    print_pause("Welcome to Mystic Market.")
    print_pause("You are an apprentice merchant trading enchanted ingredients.")
    print_pause("Your goal is to earn enough gold before the market closes.")


def make_shop():
    return {
        "gold": 12,
        "stock": {"ember petals": 0, "moon dew": 0, "star crystals": 0},
        "potions": 0,
        "day": 1,
        "goal": 30,
    }


def prices_for_day(day):
    return {
        "ember petals": random.randint(2, 5) + (day - 1),
        "moon dew": random.randint(3, 6) - (day // 2),
        "star crystals": random.randint(4, 8) - (day // 3),
    }


def show_status(shop, prices):
    print_pause(f"\nDay {shop['day']} of 5")
    print_pause(f"Gold: {shop['gold']} | Potions: {shop['potions']}")
    print_pause("Stock:")
    for item, count in shop['stock'].items():
        print_pause(f"  {item}: {count}")
    print_pause("Today's market prices:")
    for item, price in prices.items():
        print_pause(f"  {item}: {price} gold")


def buy_ingredient(shop, prices):
    print_pause("What would you like to buy?")
    item = get_choice("ember petals/moon dew/star crystals/back: ", ["ember petals", "moon dew", "star crystals", "back"])
    if item == "back":
        return
    cost = prices[item]
    if shop['gold'] >= cost:
        shop['gold'] -= cost
        shop['stock'][item] += 1
        print_pause(f"You buy 1 {item} for {cost} gold.")
    else:
        print_pause("Not enough gold.")


def sell_ingredient(shop, prices):
    print_pause("What would you like to sell?")
    item = get_choice("ember petals/moon dew/star crystals/back: ", ["ember petals", "moon dew", "star crystals", "back"])
    if item == "back":
        return
    if shop['stock'][item] > 0:
        price = max(1, prices[item] - 1)
        shop['stock'][item] -= 1
        shop['gold'] += price
        print_pause(f"You sell 1 {item} for {price} gold.")
    else:
        print_pause(f"You have no {item} to sell.")


def craft_potion(shop):
    recipe = {"ember petals": 1, "moon dew": 1, "star crystals": 1}
    can_make = all(shop['stock'][item] >= count for item, count in recipe.items())
    if not can_make:
        print_pause("You do not have the right blend yet.")
        return
    for item, count in recipe.items():
        shop['stock'][item] -= count
    shop['potions'] += 1
    print_pause("You brew a glowing potion.")


def rest_day(shop):
    shop['day'] += 1
    print_pause("You wait for the market to shift.")


def end_of_day(shop):
    shop['day'] += 1
    print_pause("The market closes for the day.")


def play_market():
    intro()
    shop = make_shop()
    while shop['day'] <= 5 and shop['gold'] < shop['goal']:
        prices = prices_for_day(shop['day'])
        show_status(shop, prices)
        action = get_choice("Action? buy/sell/craft/rest/status/quit: ", ["buy", "sell", "craft", "rest", "status", "quit"])
        if action == "buy":
            buy_ingredient(shop, prices)
        elif action == "sell":
            sell_ingredient(shop, prices)
        elif action == "craft":
            craft_potion(shop)
        elif action == "rest":
            rest_day(shop)
        elif action == "status":
            print_pause("Checking your ledger...")
        else:
            print_pause("You leave the market early.")
            break
        if action != "status":
            end_of_day(shop)
    if shop['gold'] >= shop['goal']:
        print_pause(f"You earned {shop['gold']} gold and won the Mystic Market challenge!")
    else:
        print_pause(f"The market closes. You leave with {shop['gold']} gold.")
        if shop['gold'] >= 18:
            print_pause("Not bad for your first week as an apprentice.")
        else:
            print_pause("Try again and plan your trades more carefully.")


def main():
    while True:
        play_market()
        again = get_choice("Play again? (yes/no): ", ["yes", "no"])
        if again == "no":
            print_pause("Thanks for visiting Mystic Market!")
            break


if __name__ == "__main__":
    main()
