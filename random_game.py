import random

def guessing_game():
    """Guess the number game"""
    print("\n🎯 GUESSING GAME")
    print("-" * 30)
    secret = random.randint(1, 100)
    guesses = 0
    
    while True:
        guess = int(input("Guess a number (1-100): "))
        guesses += 1
        
        if guess < secret:
            print("Too low! Try again.")
        elif guess > secret:
            print("Too high! Try again.")
        else:
            print(f"🎉 Correct! You got it in {guesses} guesses!")
            return guesses

def rock_paper_scissors():
    """Rock Paper Scissors game"""
    print("\n✂️ ROCK PAPER SCISSORS")
    print("-" * 30)
    choices = ["rock", "paper", "scissors"]
    wins = 0
    
    for round_num in range(3):
        player = input(f"Round {round_num + 1}: Enter rock, paper, or scissors: ").lower()
        computer = random.choice(choices)
        
        print(f"Computer chose: {computer}")
        
        if player == computer:
            print("It's a tie!")
        elif (player == "rock" and computer == "scissors") or \
             (player == "paper" and computer == "rock") or \
             (player == "scissors" and computer == "paper"):
            print("You win this round! ✅")
            wins += 1
        else:
            print("You lose this round! ❌")
    
    print(f"Final: You won {wins}/3 rounds!")
    return wins

def math_quiz():
    """Random math questions"""
    print("\n🧮 MATH QUIZ")
    print("-" * 30)
    score = 0
    
    for question_num in range(5):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(["+", "-", "*"])
        
        if operation == "+":
            correct_answer = num1 + num2
        elif operation == "-":
            correct_answer = num1 - num2
        else:  # *
            correct_answer = num1 * num2
        
        answer = int(input(f"Question {question_num + 1}: {num1} {operation} {num2} = "))
        
        if answer == correct_answer:
            print("Correct! ✅")
            score += 1
        else:
            print(f"Wrong! The answer was {correct_answer} ❌")
    
    print(f"Final Score: {score}/5")
    return score

def trivia_game():
    """Random trivia questions"""
    print("\n🧠 TRIVIA GAME")
    print("-" * 30)
    
    questions = [
        ("What is the capital of France?", "paris", 1),
        ("How many continents are there?", "7", 1),
        ("What is 2 + 2?", "4", 1),
        ("What color is the sky?", "blue", 1),
        ("How many legs does a dog have?", "4", 1),
    ]
    
    score = 0
    for q, answer, points in random.sample(questions, 3):
        user_answer = input(f"{q} ").lower()
        if user_answer == answer:
            print("Correct! ✅")
            score += points
        else:
            print(f"Wrong! Answer: {answer} ❌")
    
    print(f"Final Score: {score} points")
    return score

def coin_flip_game():
    """Flip a coin and guess"""
    print("\n🪙 COIN FLIP GAME")
    print("-" * 30)
    score = 0
    
    for round_num in range(5):
        guess = input(f"Round {round_num + 1} - Heads or Tails? ").lower()
        flip = random.choice(["heads", "tails"])
        
        print(f"The coin landed on: {flip}")
        if guess == flip:
            print("You got it! ✅")
            score += 1
        else:
            print("Wrong! ❌")
    
    print(f"Final Score: {score}/5")
    return score

def dice_roller():
    """Roll dice and try to get high numbers"""
    print("\n🎲 DICE ROLLER")
    print("-" * 30)
    total = 0
    
    for round_num in range(5):
        input(f"Round {round_num + 1} - Press Enter to roll the dice...")
        roll = random.randint(1, 6)
        print(f"You rolled: {roll} 🎲")
        total += roll
    
    print(f"Total Score: {total}")
    return total

def hangman_game():
    """Simple hangman game"""
    print("\n🎮 HANGMAN")
    print("-" * 30)
    
    words = ["python", "computer", "random", "gaming", "adventure", "function"]
    secret_word = random.choice(words)
    guessed_letters = []
    wrong_guesses = 0
    max_wrong = 6
    
    while wrong_guesses < max_wrong:
        display = "".join([letter if letter in guessed_letters else "_" for letter in secret_word])
        print(f"Word: {display} | Wrong guesses: {wrong_guesses}/{max_wrong}")
        
        if display == secret_word:
            print(f"🎉 You won! The word was: {secret_word}")
            return 1
        
        guess = input("Guess a letter: ").lower()
        
        if guess in guessed_letters:
            print("You already guessed that!")
            continue
        
        guessed_letters.append(guess)
        
        if guess not in secret_word:
            print("Wrong! ❌")
            wrong_guesses += 1
        else:
            print("Correct! ✅")
    
    print(f"Game Over! The word was: {secret_word}")
    return 0

def main():
    """Pick a random game and play it!"""
    print("=" * 40)
    print("🎮 RANDOM GAME SELECTOR 🎮")
    print("=" * 40)
    
    games = [
        ("Guessing Game", guessing_game),
        ("Rock Paper Scissors", rock_paper_scissors),
        ("Math Quiz", math_quiz),
        ("Trivia Game", trivia_game),
        ("Coin Flip Game", coin_flip_game),
        ("Dice Roller", dice_roller),
        ("Hangman", hangman_game),
    ]
    
    # Pick a random game
    game_name, game_func = random.choice(games)
    
    print(f"\n🎲 Today you're playing: {game_name}! 🎲\n")
    
    try:
        game_func()
    except ValueError:
        print("Invalid input! Game ended.")
    
    # Ask if they want another random game
    while True:
        again = input("\n\nWant to play another random game? (yes/no): ").lower()
        if again in ["yes", "y"]:
            print("\n" * 2)
            main()
            break
        elif again in ["no", "n"]:
            print("Thanks for playing! Goodbye! 👋")
            break
        else:
            print("Please enter 'yes' or 'no'")

if __name__ == "__main__":
    main()
