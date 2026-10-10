import random

def hangman():
    words = ["python", "coding", "hangman", "developer", "program"]
    word = random.choice(words)
    guessed = ["_"] * len(word)
    attempts = 6
    guessed_letters = []

    print("🎯 Welcome to Hangman!")
    print(" ".join(guessed))

    while attempts > 0 and "_" in guessed:
        guess = input("\nEnter a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("⚠️ Please enter only one letter.")
            continue

        if guess in guessed_letters:
            print("You've already guessed that letter.")
            continue

        guessed_letters.append(guess)

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed[i] = guess
            print("✅ Correct guess!")
        else:
            attempts -= 1
            print(f"❌ Wrong guess! Attempts left: {attempts}")

        print(" ".join(guessed))

    if "_" not in guessed:
        print("\n🎉 Congratulations! You guessed the word:", word)
    else:
        print("\n💀 Game Over! The word was:", word)

if __name__ == "__main__":
    hangman()
