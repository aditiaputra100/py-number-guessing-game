from enum import Enum
import random
import threading
import time

# Event trigger user guess
event = threading.Event()
rolling_event = threading.Event()

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
    life = chances

    while 0 < chances and not event.is_set():
        try:
            # Input user guess
            input_guess: int = int(input('Enter your guess: '))

            if event.is_set():
                rolling_event.set()
                break

            if input_guess == random_number:
                print(f'Congratulations! You guessed the correct number in {life - chances} attempts.')
                event.set()
                rolling_event.set()
                break

            print(f'Incorrect! The number is {'less' if input_guess >= random_number else 'greater'} {input_guess}')

            chances -= 1
        except ValueError:
            if event.is_set():
                rolling_event.set()
                break

            print("Error: please enter valid number.")
    else:
        event.set()
        rolling_event.set()
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
    game_thread.daemon = True
    game_thread.start()

    # Start timer
    timer_thread = threading.Thread(target=start_timer, args=(difficulty_choice.value[1],))
    timer_thread.start()

    game_thread.join(timeout=difficulty_choice.value[1])

    if game_thread.is_alive():
        event.set()
        print("\nTime's up!")
        print(f'Sorry.. the correct number is {random_number}')
        print('Press enter to continue..')
        game_thread.join()


def main():
    while True:
        # Start the game
        random_number = random.randint(1, 100)

        start_game(random_number)

        while rolling_event.is_set():
            # Rolling game
            user_input = input("Do you want to play again? (y/n) ").lower()

            while user_input not in ['y', 'n']:
                print('Error: please enter the correct answer')
                user_input = input("Do you want to play again? (y/n) ").lower()

            if user_input == 'n':
                exit(0)

            if user_input == 'y':
                rolling_event.clear()
                event.clear()
                break

if __name__ == '__main__':
    main()