"""
Day 2 Exercises: Python Fundamentals
-------------------------------------
1. Score to letter grade converter
2. FizzBuzz 1-100 generator
3. Password strength checker
4. Number guessing game using random
5. Custom title case converter (without string.title())
"""

import random
import string


def get_letter_grade(score: float) -> str:
    """Returns a letter grade based on numerical score (0-100)."""
    if not isinstance(score, (int, float)):
        raise TypeError("Score must be a number.")
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100.")

    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def fizzbuzz(n: int = 100) -> list[str]:
    """Returns a list of FizzBuzz results from 1 to n."""
    results = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            results.append("FizzBuzz")
        elif i % 3 == 0:
            results.append("Fizz")
        elif i % 5 == 0:
            results.append("Buzz")
        else:
            results.append(str(i))
    return results


def check_password_strength(password: str) -> list[str]:
    """Checks password strength against rules and returns a list of issues.
    
    Rules:
    - Minimum length 8 characters
    - Must contain at least one digit
    - Must contain at least one uppercase letter
    - Must contain at least one special symbol
    """
    problems = []
    if len(password) < 8:
        problems.append("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        problems.append("Password must contain at least one digit.")
    if not any(char.isupper() for char in password):
        problems.append("Password must contain at least one uppercase letter.")
    if not any(char in string.punctuation for char in password):
        problems.append("Password must contain at least one special symbol.")
    return problems


def number_guessing_game(secret_number: int = None, guesses: list[int] = None) -> int:
    """Plays a number guessing game between 1 and 100.
    
    Can accept a fixed `secret_number` and pre-defined `guesses` list for automated testing.
    Returns the total number of attempts taken.
    """
    if secret_number is None:
        secret_number = random.randint(1, 100)

    attempts = 0
    if guesses is not None:
        # Automated test mode
        for guess in guesses:
            attempts += 1
            if guess < secret_number:
                pass
            elif guess > secret_number:
                pass
            else:
                return attempts
        return attempts
    else:
        # Interactive mode
        print("Guess the secret number between 1 and 100!")
        while True:
            try:
                user_input = input("Enter your guess: ")
                guess = int(user_input)
                attempts += 1
                if guess < secret_number:
                    print("Too low!")
                elif guess > secret_number:
                    print("Too high!")
                else:
                    print(f"Congratulations! You guessed it in {attempts} attempts.")
                    return attempts
            except ValueError:
                print("Please enter a valid integer.")


def to_title_case(sentence: str) -> str:
    """Converts a string sentence to Title Case without using str.title()."""
    if not sentence:
        return ""
    
    words = sentence.split(" ")
    title_cased_words = []
    for word in words:
        if not word:
            title_cased_words.append("")
            continue
        first_char = word[0].upper()
        rest_chars = word[1:].lower()
        title_cased_words.append(first_char + rest_chars)
        
    return " ".join(title_cased_words)


if __name__ == "__main__":
    print("--- Day 2: Python Fundamentals Demo ---")

    # 1. Letter Grade Test
    test_scores = [95, 82, 74, 61, 45]
    print("1. Letter Grades:")
    for s in test_scores:
        print(f"   Score: {s} -> Grade: {get_letter_grade(s)}")

    # 2. FizzBuzz Test
    print("\n2. FizzBuzz (first 15 items):")
    print("  ", ", ".join(fizzbuzz(15)))

    # 3. Password Strength Test
    passwords = ["short", "weakpass", "WeakPass1", "StrongPass!123"]
    print("\n3. Password Strength Checker:")
    for pw in passwords:
        issues = check_password_strength(pw)
        status = "Strong" if not issues else f"Weak ({', '.join(issues)})"
        print(f"   '{pw}': {status}")

    # 4. Number Guessing Game (Automated simulation)
    secret = 42
    sample_guesses = [20, 60, 35, 42]
    attempts = number_guessing_game(secret_number=secret, guesses=sample_guesses)
    print(f"\n4. Number Guessing Game Simulation: Guessed secret {secret} in {attempts} attempts.")

    # 5. Title Case Test
    sample_sentence = "hello world! this IS a python SCRIPT."
    converted = to_title_case(sample_sentence)
    print(f"\n5. Title Case Converter:")
    print(f"   Original:  '{sample_sentence}'")
    print(f"   Converted: '{converted}'")
