import random

print("---------------------")
print("  M&M guessing game! ")
print("---------------------")

print("Guess the number of M&Ms and you get a prize")
print()

mm_count = random.randint(1, 100)
attempt_limit = 5
attempts = 0

while attempts < attempt_limit:
    attempts += 1
    guess_text = input("How many are in the jar? ")
    guess = int(guess_text)

    if mm_count == guess:
        print(f"winner, number was {guess}")
        break
    elif guess < mm_count:
        print("too low")
    else:
        print("Too high")

print(f"Bye, finished in {attempts} tries")
