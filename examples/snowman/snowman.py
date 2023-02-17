from wonderwords import RandomWord
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


SNOWMAN_ASCII_ART = '''
------------------------
         _[_]_
          (")
      `--( : )--'
        (  :  )
      ""`-...-'""
------------------------
'''

SNOWMAN_GRAPHIC = SNOWMAN_ASCII_ART.strip().split('\n')

GREETINGS_MESSAGE = '''
=====================================================
    Let's play a Snowman game!

    I guessed a word - try to find out what the
    word is by guessing letters!
=====================================================
'''


def draw_snowman(num_lines_to_draw):
    for i in range(len(SNOWMAN_GRAPHIC) - num_lines_to_draw, len(SNOWMAN_GRAPHIC)):
        print(SNOWMAN_GRAPHIC[i])


def get_one_character():
    ch = ''
    while len(ch) != 1:
        ch = input("Enter one letter > ").lower()
    return ch


def print_current_game_state(correct_guesses, incorrect_guesses, msg=''):
    print("SNOWMAN SO FAR:")
    print(len(SNOWMAN_GRAPHIC[0])*"=")
    for i in range(len(SNOWMAN_GRAPHIC) - len(incorrect_guesses)):
        print()
    draw_snowman(len(incorrect_guesses))
    print(len(SNOWMAN_GRAPHIC[0])*"=")
    print()

    print(msg)
    print()

    if correct_guesses:
        correct = ', '.join(f"'{x}'" for x in correct_guesses)
        print(f"Guessed correct: {correct}")
    else:
        print("No correct guesses yet.")

    if incorrect_guesses:
        incorrect = ', '.join(f"'{x}'" for x in incorrect_guesses)
        print(f"Guessed incorrectly: {incorrect}")
    else:
        print("No incorrect guesses yet.")


def collect_user_input(correct_guesses, incorrect_guesses):
    user_input = get_one_character()
    while user_input in correct_guesses or user_input  in incorrect_guesses:
        print("Enter character you haven't use before")
        user_input = get_one_character()
    return user_input


def print_end_game(is_user_won, secret_word):
    print(60*"=")
    if is_user_won:
        print("    Congratulations! You guessed all letters correctly!")
    else:
        print("    Unfortunately you lost...")
    print(f"    The word is '{secret_word}'")
    print(60*"=")


def snowman_game(word_min_length=5, word_max_length=8, show_secret_word=False):
    word_to_guess = RandomWord().word(
        word_min_length=word_min_length,
        word_max_length=word_max_length)

    letters_left_to_guess = set(word_to_guess)
    correct_guesses = []
    incorrect_guesses = []
    wrong_guesses_number = 0

    clear_screen()
    if show_secret_word:
        print('SECRET_WORD:', word_to_guess)

    print(GREETINGS_MESSAGE)
    input("Press [Enter] to continue")

    msg = ''
    while len(incorrect_guesses) < len(SNOWMAN_GRAPHIC) and letters_left_to_guess:
        clear_screen()
        print_current_game_state(correct_guesses, incorrect_guesses, msg)

        user_input = collect_user_input(correct_guesses, incorrect_guesses)
        if user_input not in letters_left_to_guess:
            incorrect_guesses.append(user_input)
            msg = 'Unfortunately there is no such letter in the secret word...'
            continue

        msg = 'Woohoo! There is such letter in the secret word!'
        correct_guesses.append(user_input)
        letters_left_to_guess.remove(user_input)

    clear_screen()
    print_current_game_state(correct_guesses, incorrect_guesses)
    print()
    print_end_game(not letters_left_to_guess, word_to_guess)


if __name__ == '__main__':
    snowman_game(show_secret_word=True)
