# Week 1 Quiz - Git and Python Core Answers

## Question 1
**What is the difference between `git add` and `git commit`?**

- **`git add`**: Moves modified or untracked files into the **Staging Area** (Index), preparing specific changes to be saved in the next snapshot.
- **`git commit`**: Takes all currently staged changes and records a permanent, immutably hashed **snapshot (commit)** in the Git repository history along with a commit message, author details, and timestamp.

---

## Question 2
**What is the difference between `git push` and `git pull`?**

- **`git push`**: Uploads local commits from your local repository branch to a remote repository (e.g., GitHub / GitLab).
- **`git pull`**: Fetches the latest commits from the remote repository branch and automatically merges them into your current local branch (`git fetch` + `git merge`).

---

## Question 3
**What is a branch, and why do we create one for each piece of work?**

A **branch** is an independent, lightweight pointer to a specific commit line in Git's commit graph. 

We create a dedicated feature branch for each piece of work to:
1. Isolate incomplete or experimental changes from the stable `main`/`master` codebase.
2. Allow multiple team members to work on different features concurrently without conflict.
3. Enable code reviews via Pull Requests (PRs) before merging code into production.

---

## Question 4
**What is the purpose of a `.gitignore` file? Name two things that belong in it for a Python project.**

A **`.gitignore`** file specifies untracked files and directories that Git should intentionally ignore and never track or commit into the repository.

Two essential things that belong in a Python `.gitignore`:
1. **Virtual environment directory**: `.venv/` or `venv/`
2. **Bytecode / Cache files**: `__pycache__/` or `*.pyc`

*(Bonus: Sensitive environment configuration files like `.env`)*

---

## Question 5
**What is the output of `[x*2 for x in range(5) if x % 2 == 0]`?**

**Output:** `[0, 4, 8]`

**Step-by-step breakdown:**
- `range(5)` generates integers: `0, 1, 2, 3, 4`
- Filter `if x % 2 == 0` selects even numbers: `0, 2, 4`
- Expression `x * 2` multiplies each selected number by 2:
  - `0 * 2 = 0`
  - `2 * 2 = 4`
  - `4 * 2 = 8`
- Resulting list: `[0, 4, 8]`

---

## Question 6
**Which is mutable: a tuple or a list? Why can a tuple be a dict key but a list cannot?**

- A **list** is mutable (its elements can be altered, added, or removed after creation).
- A **tuple** is immutable (its structure and element references cannot be changed after creation).

**Dictionary Key Requirement:**
Dictionary keys in Python must be **hashable** (their hash value remains constant throughout their lifetime). 
- **Tuples** (containing only immutable elements) are hashable and immutable, making them valid dictionary keys.
- **Lists** are mutable, meaning their contents (and potential hash value) could change during runtime, which would break hash table indexing. Thus, lists are unhashable and cannot be used as dictionary keys.

---

## Question 7
**What is the difference between `==` and `is`?**

- **`==` (Value Equality)**: Checks whether the values/contents of two objects are equal.
- **`is` (Identity Equality)**: Checks whether two variables refer to the **exact same memory address** (i.e. `id(a) == id(b)`).

*Rule of thumb:* Use `==` to compare values (e.g. `a == 5`), and use `is` when comparing against singletons like `None` (e.g., `if result is None:`).

---

## Question 8
**What do `*args` and `**kwargs` collect inside a function?**

- **`*args`**: Collects any extra **positional arguments** passed to the function into a **tuple**.
- **`**kwargs`**: Collects any extra **keyword/named arguments** passed to the function into a **dictionary**.

---

## Question 9
**Why should every project use a virtual environment?**

Every Python project should use a virtual environment (`venv`) to:
1. **Isolate dependencies**: Prevent conflicting versions of third-party libraries across different projects on the same machine.
2. **Ensure reproducibility**: Guarantee that all team members and deployment servers run the exact same dependency versions specified in `requirements.txt`.
3. **Avoid system Python pollution**: Protect the global operating system Python environment from unexpected package overwrites.

---

## Question 10
**What is wrong with `def add(item, items=[]):`?**

Default parameter values in Python are evaluated **once when the function definition is executed**, NOT each time the function is called.

Because `[]` is a **mutable default argument**, all function calls that omit the `items` parameter will reuse and mutate the **same single list object** across calls.

**Incorrect behavior:**
```python
add(1) # returns [1]
add(2) # returns [1, 2] -- Unexpected retention of previous call!
```

**Correct idiom:**
```python
def add(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```
