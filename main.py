from enum import Enum
import os
import random
import signal
import threading
import time

# Event trigger user guess
event = threading.Event()

class Difficulty(Enum):
    EASY = (10, 90)
    MEDIUM = (5, 60)
    HARD = (3, 30)

def start_timer(limit: int):
    # Set up timer
    start_time = time.time()
    time_limit = limit
    half_alerted = False

    while time.time() - start_time < time_limit:
        if event.is_set():
            break

        remaining = time.time() - start_time

        if not half_alerted and (remaining >= time_limit / 2):
            remaining = int(remaining)
            print(f'\n{remaining} seconds remaining..')
            half_alerted = True

        time.sleep(1)

def run_game(random_number: int, chances: int):
    while 0 < chances and not event.is_set():
        try:
            # Input user guess
            input_guess: int = int(input('Enter your guess: '))

            if input_guess == random_number:
                print(f'Congratulations! You guessed the correct number in {chances} attempts.')
                event.set()
                break

            print(f'Incorrect! The number is {'less' if input_guess >= random_number else 'greater'} {input_guess}')

            chances -= 1
        except ValueError:
            print("Error: please enter valid number.")
    else:
        print(f'\nSorry.. the correct number is {random_number}')

def start_game(random_number: int):
    welcome_script: str = '''Welcome to the Number Guessing Game!
        \rI'm thinking of a number between 1 and 100.
        \rYou have 5 chances to guess the correct number.
        '''

    # Print welcome script
    print(welcome_script)

    # Select difficulty level
    difficulty_chances: dict[str, tuple[int, int]] = {
        'easy': (10, 90),
        'medium': (5, 60),
        'hard': (3, 30),
    }
    print('Please select the difficulty level:')

    for index, (difficulty, (chances, times)) in enumerate(difficulty_chances.items()):
        print(f'{index + 1}. {difficulty.capitalize()} ({chances} chances) ({times} seconds)')

    # Input choice
    input_choice: int = int(input("Enter your choice: "))

    difficulty_choice = Difficulty.EASY if input_choice == 1 else Difficulty.MEDIUM if input_choice == 2 else Difficulty.HARD

    print(f"Great! You have selected the {difficulty_choice.name} difficulty level.")
    print("Let's start the game!")

    user_chances: int = difficulty_choice.value[0]

    game_thread = threading.Thread(target=run_game, args=(random_number, user_chances))
    game_thread.start()

    # Start timer
    timer_thread = threading.Thread(target=start_timer, args=(difficulty_choice.value[1],))
    timer_thread.start()

    game_thread.join(timeout=difficulty_choice.value[1])

    if game_thread.is_alive():
        print("\nTime's up! Terminating game...")
        print(f'Sorry.. the correct number is {random_number}')
        os.kill(os.getpid(), signal.SIGINT)


def main():
    # Start the game
    random_number = random.randint(1, 100)

    start_game(random_number)

if __name__ == '__main__':
    main()