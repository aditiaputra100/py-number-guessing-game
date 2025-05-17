from enum import Enum
import random


class Difficulty(Enum):
    EASY = 10
    MEDIUM = 5
    HARD = 3

def main():
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
        print(f'{index + 1}. {difficulty.capitalize()} ({chances} chances)')

    # Input choice
    input_choice: int = int(input("Enter your choice: " ))

    difficulty_choice = Difficulty.EASY if input_choice == 1 else Difficulty.MEDIUM if input_choice == 2 else Difficulty.HARD

    print(f"Great! You have selected the {difficulty_choice.name} difficulty level.")
    print("Let's start the game!")

    # Start the game
    random_number = random.randint(1, 100)

    user_chances: int = difficulty_choice.value
    is_correct: bool = False

    while 0 < user_chances:
        # Input user guess
        input_guess: int = int(input('Enter your guess: '))

        if input_guess == random_number:
            is_correct = True
            break


        print(f'Incorrect! The number is {'less' if input_guess >= random_number else 'greater'} {input_guess}')

        user_chances -= 1

    if is_correct:
        print(f'Congratulations! You guessed the correct number in {user_chances} attempts.')
    else:
        print(f'Sorry.. the correct number is {random_number}')

if __name__ == '__main__':
    main()