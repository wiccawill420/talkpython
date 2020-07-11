import random


def main():
    print_head()
    play()


def print_head():
    print('#######################')
    print('#  M&M Guessing Game  #')
    print('#######################')
    print("Guess the number of M&Ms and you get a prize (1-100)")
    print()


def play():
    mm_count = random.randint(1, 100)
    attempt_limit = 5
    attempts = 0

    while attempts < attempt_limit:
        attempts += 1
        guess_text = input("What is your guess? ")
        guess = int(guess_text)

        if mm_count == guess:
            print(f"winner, number was {guess}")
            break
        elif guess < mm_count:
            print("too low")
        else:
            print("Too high")

    print(f"Nope, it was {mm_count}")
    print(f"Bye, finished in {attempts} tries")


if __name__ == '__main__':
    main()
