"""
Storage module for Expense Tracker.
Handles JSON persistence and CSV file export operations.
"""

import csv
import json
from pathlib import Path
from typing import Optional


DEFAULT_STORAGE_FILE = Path(__file__).parent / "expenses.json"


class StorageError(Exception):
    """Custom exception raised when storage operations fail."""
    pass


def load_expenses(filepath: Optional[Path] = None) -> list[dict]:
    """Loads expenses from a JSON file.

    Returns an empty list if file does not exist.
    """
    path = filepath or DEFAULT_STORAGE_FILE
    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as e:
        raise StorageError(f"Failed to read expenses storage file '{path}': {e}")


def save_expenses(expenses: list[dict], filepath: Optional[Path] = None) -> None:
    """Saves expenses list to a JSON file."""
    path = filepath or DEFAULT_STORAGE_FILE
    try:
        # Create parent directory if missing
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2, ensure_ascii=False)
    except OSError as e:
        raise StorageError(f"Failed to save expenses to storage file '{path}': {e}")


def get_next_id(expenses: list[dict]) -> int:
    """Returns the next auto-incrementing integer ID."""
    if not expenses:
        return 1
    existing_ids = [e.get("id", 0) for e in expenses if isinstance(e.get("id"), int)]
    return max(existing_ids, default=0) + 1


def export_to_csv(expenses: list[dict], output_filepath: Path) -> None:
    """Exports expenses list to a CSV file."""
    try:
        output_filepath.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = ["id", "amount", "category", "date", "note"]
        with open(output_filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for expense in expenses:
                writer.writerow({
                    "id": expense.get("id"),
                    "amount": f"{expense.get('amount', 0.0):.2f}",
                    "category": expense.get("category", ""),
                    "date": expense.get("date", ""),
                    "note": expense.get("note", "")
                })
    except OSError as e:
        raise StorageError(f"Failed to export expenses to CSV file '{output_filepath}': {e}")
