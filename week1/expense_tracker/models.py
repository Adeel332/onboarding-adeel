"""
Models module for Expense Tracker.
Handles expense data structures, validation, and calculations.
"""

from datetime import datetime
from typing import Optional


class ExpenseValidationError(Exception):
    """Custom exception raised when expense validation fails."""
    pass


def create_expense(
    amount: float,
    category: str,
    date_str: Optional[str] = None,
    note: str = "",
    expense_id: Optional[int] = None
) -> dict:
    """Builds and validates an expense dictionary.

    Args:
        amount: Numerical amount of expense (must be positive).
        category: Category name (e.g. Food, Transport, Utilities).
        date_str: Date in YYYY-MM-DD format (defaults to current date if None).
        note: Optional memo/description.
        expense_id: Unique integer ID.

    Returns:
        Validated expense dictionary.

    Raises:
        ExpenseValidationError: If validation fails for amount, category, or date format.
    """
    # Validate Amount
    try:
        val_amount = float(amount)
    except (ValueError, TypeError):
        raise ExpenseValidationError(f"Invalid amount '{amount}'. Amount must be a valid positive number.")
    
    if val_amount <= 0:
        raise ExpenseValidationError(f"Invalid amount '{val_amount}'. Amount must be strictly greater than 0.")

    # Validate Category
    clean_category = str(category).strip()
    if not clean_category:
        raise ExpenseValidationError("Category cannot be empty.")

    # Validate Date
    if date_str is None or not str(date_str).strip():
        val_date = datetime.now().strftime("%Y-%m-%d")
    else:
        clean_date = str(date_str).strip()
        try:
            parsed_date = datetime.strptime(clean_date, "%Y-%m-%d")
            val_date = parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            raise ExpenseValidationError(
                f"Invalid date format '{clean_date}'. Expected format YYYY-MM-DD (e.g. 2026-09-29)."
            )

    return {
        "id": expense_id,
        "amount": round(val_amount, 2),
        "category": clean_category,
        "date": val_date,
        "note": note.strip() if note else ""
    }


def calculate_category_summary(expenses: list[dict]) -> dict[str, float]:
    """Calculates total expense amount grouped by category."""
    summary = {}
    for expense in expenses:
        cat = expense["category"]
        amt = expense["amount"]
        summary[cat] = round(summary.get(cat, 0.0) + amt, 2)
    return summary
