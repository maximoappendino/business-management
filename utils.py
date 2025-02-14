import re
import os
from termcolor import colored

def validate_positive_number(value):
    """Ensures the given value is a positive number."""
    try:
        num = float(value)
        return num > 0
    except ValueError:
        return False

def validate_code_format(code):
    """Checks if the code follows a valid alphanumeric format."""
    return bool(re.match(r'^[A-Za-z0-9_-]+$', code))

def format_currency(amount):
    """Formats a number into a currency-style string."""
    return f"${amount:,.2f}"

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color="green"):
    """Prints text in a specified color."""
    print(colored(text, color))

