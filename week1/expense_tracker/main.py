"""
Main CLI entrypoint for Expense Tracker.
Uses argparse to process commands: add, list, summary, export.
Handles errors gracefully with clean output messages without tracebacks.
"""

import argparse
from pathlib import Path
import sys

from models import (
    ExpenseValidationError,
    calculate_category_summary,
    create_expense,
)
from storage import (
    StorageError,
    export_to_csv,
    get_next_id,
    load_expenses,
    save_expenses,
)


def handle_add(args: argparse.Namespace) -> None:
    """Handles 'add' command."""
    expenses = load_expenses()
    next_id = get_next_id(expenses)
    
    expense = create_expense(
        amount=args.amount,
        category=args.category,
        date_str=args.date,
        note=args.note,
        expense_id=next_id
    )
    
    expenses.append(expense)
    save_expenses(expenses)
    
    print(f"[+] Expense added successfully! (ID: {expense['id']}, Amount: ${expense['amount']:.2f}, Category: '{expense['category']}', Date: {expense['date']})")


def handle_list(args: argparse.Namespace) -> None:
    """Handles 'list' command with optional filtering by month or category."""
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    filtered = expenses
    if args.month:
        month_filter = args.month.strip()
        filtered = [e for e in filtered if e.get("date", "").startswith(month_filter)]

    if args.category:
        cat_filter = args.category.strip().lower()
        filtered = [e for e in filtered if e.get("category", "").lower() == cat_filter]

    if not filtered:
        print("No matching expenses found for the specified filters.")
        return

    print("\n" + "=" * 65)
    print(f"{'ID':<5} | {'Date':<10} | {'Category':<15} | {'Amount ($)':<10} | {'Note'}")
    print("=" * 65)
    total = 0.0
    for e in filtered:
        amt = e.get("amount", 0.0)
        total += amt
        print(f"{e.get('id', '-'):<5} | {e.get('date', ''):<10} | {e.get('category', ''):<15} | {amt:<10.2f} | {e.get('note', '')}")
    print("=" * 65)
    print(f"Total Amount: ${total:.2f} ({len(filtered)} items)\n")


def handle_summary(args: argparse.Namespace) -> None:
    """Handles 'summary' command showing total expenses by category."""
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    if args.month:
        month_filter = args.month.strip()
        expenses = [e for e in expenses if e.get("date", "").startswith(month_filter)]
        if not expenses:
            print(f"No expenses found for month {month_filter}.")
            return

    summary = calculate_category_summary(expenses)
    grand_total = sum(summary.values())

    print("\n" + "=" * 45)
    header = "Category Expense Summary"
    if args.month:
        header += f" ({args.month})"
    print(f"{header:^45}")
    print("=" * 45)
    for category, amount in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / grand_total * 100) if grand_total > 0 else 0.0
        print(f" - {category:<20}: ${amount:>8.2f} ({percentage:>5.1f}%)")
    print("-" * 45)
    print(f"  {'Grand Total':<20}: ${grand_total:>8.2f}")
    print("=" * 45 + "\n")


def handle_export(args: argparse.Namespace) -> None:
    """Handles 'export' command to CSV."""
    expenses = load_expenses()
    if not expenses:
        print("No expenses available to export.")
        return

    output_path = Path(args.output)
    export_to_csv(expenses, output_path)
    print(f"[+] Successfully exported {len(expenses)} expenses to '{output_path}'.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Expense Tracker CLI - Track your daily expenses efficiently.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: add
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("-a", "--amount", required=True, type=float, help="Expense amount (positive number)")
    add_parser.add_argument("-c", "--category", required=True, type=str, help="Category name (e.g. Food, Rent, Tech)")
    add_parser.add_argument("-d", "--date", type=str, default=None, help="Expense date in YYYY-MM-DD format (defaults to today)")
    add_parser.add_argument("-n", "--note", type=str, default="", help="Optional description/note")

    # Command: list
    list_parser = subparsers.add_parser("list", help="List recorded expenses")
    list_parser.add_argument("-m", "--month", type=str, help="Filter expenses by month (YYYY-MM)")
    list_parser.add_argument("-c", "--category", type=str, help="Filter expenses by category")

    # Command: summary
    summary_parser = subparsers.add_parser("summary", help="Show total expenses grouped by category")
    summary_parser.add_argument("-m", "--month", type=str, help="Filter summary by month (YYYY-MM)")

    # Command: export
    export_parser = subparsers.add_parser("export", help="Export expenses to CSV file")
    export_parser.add_argument("-o", "--output", type=str, default="expenses_export.csv", help="CSV output filename (default: expenses_export.csv)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        if args.command == "add":
            handle_add(args)
        elif args.command == "list":
            handle_list(args)
        elif args.command == "summary":
            handle_summary(args)
        elif args.command == "export":
            handle_export(args)
    except ExpenseValidationError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except StorageError as e:
        print(f"Storage Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
