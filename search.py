import os
import sqlite3
from rapidfuzz import process

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "inventory.db")

def search_by_code(code):
    """Search for an item by exact code."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT code, title, amount, purchase_price, provider FROM inventory WHERE code = ?", (code,))
    result = cursor.fetchall()
    conn.close()
    return result

def search_by_title(title):
    """Search for an item using fuzzy matching on the title."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM inventory")
    titles = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    matches = process.extract(title, titles, limit=5)
    return [match[0] for match in matches]

def search_menu():
    """Search menu for user interaction."""
    while True:
        print("\nSEARCH MENU")
        print("1. Search by Code")
        print("2. Search by Title")
        print("Q. Quit")
        
        choice = input("Select an option: ").strip().lower()
        
        if choice == '1':
            code = input("Enter the item code: ").strip()
            results = search_by_code(code)
            if results:
                for item in results:
                    print(f"{item[0]} | {item[1]} | {item[2]} | ${item[3]} | {item[4]}")
            else:
                print("No items found.")
        
        elif choice == '2':
            title = input("Enter part of the title: ").strip()
            results = search_by_title(title)
            if results:
                print("Possible matches:")
                for result in results:
                    print(f"- {result}")
            else:
                print("No matches found.")
        
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    search_menu()

