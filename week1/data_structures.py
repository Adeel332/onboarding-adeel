"""
Day 3 Exercises: Python Data Structures
---------------------------------------
1. Word counter (10 most frequent words ignoring punctuation and case)
2. Contacts cleaner (deduplicate contacts by email, sort by name)
3. Marks report (student averages & class topper using comprehensions)
4. 5 Exercism-style Python track exercises:
   - Isogram check
   - Anagram check
   - Flatten nested list
   - Matrix transpose
   - Difference of squares
"""

from collections import Counter
import re


# -----------------------------------------------------------------------------
# Exercise 1: Word Counter
# -----------------------------------------------------------------------------
def word_counter(paragraph: str, top_n: int = 10) -> list[tuple[str, int]]:
    """Reads a paragraph and returns the top_n most frequent words ignoring case & punctuation."""
    # Strip punctuation and convert to lowercase
    words = re.findall(r"\b[a-zA-Z0-9]+\b", paragraph.lower())
    counts = Counter(words)
    return counts.most_common(top_n)


# -----------------------------------------------------------------------------
# Exercise 2: Contacts Cleaner
# -----------------------------------------------------------------------------
def clean_contacts(contacts: list[dict[str, str]]) -> list[dict[str, str]]:
    """Given a list of contact dicts, returns unique contacts (by email) sorted by name.
    
    Each contact dict has keys: 'name', 'email', 'phone'.
    """
    seen_emails = set()
    unique_contacts = []
    
    for contact in contacts:
        email = contact.get("email", "").strip().lower()
        if email and email not in seen_emails:
            seen_emails.add(email)
            unique_contacts.append({
                "name": contact.get("name", "").strip(),
                "email": email,
                "phone": contact.get("phone", "").strip()
            })
            
    # Sort contacts by name alphabetically
    return sorted(unique_contacts, key=lambda c: c["name"])


# -----------------------------------------------------------------------------
# Exercise 3: Marks Report
# -----------------------------------------------------------------------------
def produce_marks_report(student_marks: dict[str, list[float]]) -> tuple[dict[str, float], str, float]:
    """Given a dict mapping student names to list of marks:
    - Produces average mark per student using dict comprehension.
    - Finds the class topper (highest average mark).
    Returns (averages_dict, topper_name, topper_avg).
    """
    if not student_marks:
        return {}, "", 0.0

    # Dict comprehension for student averages
    student_averages = {
        student: round(sum(marks) / len(marks), 2) if marks else 0.0
        for student, marks in student_marks.items()
    }
    
    # Class topper
    topper = max(student_averages, key=student_averages.get)
    return student_averages, topper, student_averages[topper]


# -----------------------------------------------------------------------------
# Exercise 4: 5 Exercism Python Track Exercises
# -----------------------------------------------------------------------------
def is_isogram(phrase: str) -> bool:
    """Check if a string has no repeating letters (case-insensitive, ignoring spaces/hyphens)."""
    clean_chars = [c.lower() for c in phrase if c.isalpha()]
    return len(clean_chars) == len(set(clean_chars))


def is_anagram(word1: str, word2: str) -> bool:
    """Check if word1 and word2 are anagrams of each other (case-insensitive)."""
    w1, w2 = word1.lower(), word2.lower()
    if w1 == w2:
        return False
    return sorted(w1) == sorted(w2)


def flatten_list(nested: list) -> list:
    """Flattens an arbitrarily nested list structure."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        elif item is not None:
            result.append(item)
    return result


def transpose_matrix(matrix: list[list]) -> list[list]:
    """Transposes a 2D matrix using zip and list comprehensions."""
    if not matrix or not matrix[0]:
        return []
    return [list(column) for column in zip(*matrix)]


def difference_of_squares(n: int) -> int:
    """Calculates the difference between the square of sum and sum of squares of first n numbers.
    Square of sum: (1 + 2 + ... + n)^2
    Sum of squares: 1^2 + 2^2 + ... + n^2
    """
    square_of_sum = sum(range(1, n + 1)) ** 2
    sum_of_squares = sum(x ** 2 for x in range(1, n + 1))
    return square_of_sum - sum_of_squares


# -----------------------------------------------------------------------------
# Demo & Execution
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- Day 3: Data Structures Demo ---\n")

    # 1. Word Counter Demo
    sample_paragraph = (
        "Python is an amazing language. Python is simple, powerful, and fun! "
        "Learning Python data structures like lists, dicts, sets, and tuples makes Python code clean."
    )
    print("1. Top Words in Paragraph:")
    for word, count in word_counter(sample_paragraph, top_n=5):
        print(f"   '{word}': {count}")

    # 2. Contacts Cleaner Demo
    sample_contacts = [
        {"name": "Alice Smith", "email": "alice@example.com", "phone": "123-456"},
        {"name": "Bob Jones", "email": "bob@example.com", "phone": "987-654"},
        {"name": "Alice S.", "email": "ALICE@example.com", "phone": "000-000"},  # duplicate email
        {"name": "Charlie Brown", "email": "charlie@example.com", "phone": "555-555"},
    ]
    print("\n2. Cleaned Unique Contacts (Sorted by Name):")
    cleaned = clean_contacts(sample_contacts)
    for c in cleaned:
        print(f"   {c['name']} <{c['email']}> - {c['phone']}")

    # 3. Marks Report Demo
    marks_data = {
        "Alice": [88, 92, 95, 90],
        "Bob": [75, 80, 78, 82],
        "Charlie": [95, 98, 92, 96],
        "Diana": [85, 89, 90, 88]
    }
    averages, topper, topper_avg = produce_marks_report(marks_data)
    print("\n3. Marks Report:")
    print(f"   Averages: {averages}")
    print(f"   Class Topper: {topper} with average {topper_avg}")

    # 4. Exercism Track Exercises Demo
    print("\n4. Exercism Track Exercises:")
    print(f"   - Isogram 'lumberjack': {is_isogram('lumberjack')}")
    print(f"   - Isogram 'alphabet':   {is_isogram('alphabet')}")
    print(f"   - Anagram ('listen', 'silent'): {is_anagram('listen', 'silent')}")
    print(f"   - Flatten list [1, [2, [3, 4], 5], 6]: {flatten_list([1, [2, [3, 4], 5], 6])}")
    matrix = [[1, 2, 3], [4, 5, 6]]
    print(f"   - Matrix transpose {matrix} -> {transpose_matrix(matrix)}")
    print(f"   - Difference of squares (1 to 10): {difference_of_squares(10)}")
