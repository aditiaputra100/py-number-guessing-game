from enum import Enum
import random
import json
import os

FILE_NAME = 'highscores.json'

class Difficulty(Enum):
    EASY = 10
    MEDIUM = 5
    HARD = 3

def load_highscores():
    if not os.path.exists(FILE_NAME):
        return {d.name: None for d in Difficulty}

    with open(FILE_NAME, 'r') as file_json:
        return json.load(file_json)

def save_highscores(highscores):
    with open(FILE_NAME, 'w') as file_json:
        json.dump(highscores, file_json, indent=4)

def main():
    highscores: dict | None = load_highscores()

    welcome_script: str = '''Welcome to the Number Guessing Game!
    \rI'm thinking of a number between 1 and 100.
    \rYou have 5 chances to guess the correct number.
    '''

    # Print welcome script
    print(welcome_script)

    # Select difficulty level
    difficulty_chances: dict[str, int] = {
        'easy': 10,
        'medium': 5,
        'hard': 3,
    }
    print('Please select the difficulty level:')

    for index, (difficulty, chances) in enumerate(difficulty_chances.items()):

        best_score = highscores.get(difficulty.upper())
        best_score_str = f' | Best: {best_score if best_score else 0} tries'

        print(f'{index + 1}. {difficulty.capitalize()} ({chances} chances)', best_score_str if highscores is not None else '')

    # Input choice
    input_choice: int = int(input("Enter your choice: " ))

    difficulty_choice = Difficulty.EASY if input_choice == 1 else Difficulty.MEDIUM if input_choice == 2 else Difficulty.HARD

    print(f"Great! You have selected the {difficulty_choice.name} difficulty level.")
    print("Let's start the game!")

    # Start the game
    random_number = random.randint(1, 100)

    user_chances: int = difficulty_choice.value
    is_correct: bool = False

    life = user_chances + 1

    while 0 < user_chances:
        # Input user guess
        input_guess: int = int(input('Enter your guess: '))

        if input_guess == random_number:
            is_correct = True
            break


        print(f'Incorrect! The number is {'less' if input_guess >= random_number else 'greater'} {input_guess}')

        user_chances -= 1

    if is_correct:
        chances = life - user_chances

        print(f'Congratulations! You guessed the correct number in {chances} attempts.')
        best_score = highscores.get(difficulty_choice.name)

        if best_score is None or chances < best_score:
            highscores[difficulty_choice.name] = chances
            save_highscores(highscores)

            print('New best score!!!')
    else:
        print(f'Sorry.. the correct number is {random_number}')

if __name__ == '__main__':
    main()