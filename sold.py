import os
import sqlite3
import subprocess

# Configuration
EDITOR = "vim"  # Change to your preferred editor
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "inventory.db")

def sold_list_menu():
    """Displays the sold items list menu."""
    sort_by = {
        "date": "timestamp",
        "price": "price",
        "amount": "amount",
        "title": "title",
        "provider": "provider"
    }

    while True:
        print("\nSOLD ITEMS MENU")
        print("1. Sort by Date")
        print("2. Sort by Price")
        print("3. Sort by Amount")
        print("4. Sort by Title")
        print("5. Sort by Provider")
        print("Q. Quit")
        
        choice = input("Select an option: ").strip().lower()
        
        if choice == 'q':
            break
        if choice == '1':
            sold_list_items(sort_by["date"])
        elif choice == '2':
            sold_list_items(sort_by["price"])
        elif choice == '3':
            sold_list_items(sort_by["amount"])
        elif choice == '4':
            sold_list_items(sort_by["title"])
        elif choice == '5':
            sold_list_items(sort_by["provider"])
        else:
            print("Invalid choice. Try again.")
            continue

def sold_list_items(sort_by):
    """Lists sold items sorted by the given parameter."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor() 
    
    query = f"""
    SELECT 
        t.code, 
        i.title, 
        t.amount, 
        t.price, 
        i.provider, 
        t.timestamp
    FROM transactions t
    JOIN inventory i ON t.code = i.code
    WHERE t.transaction_type = 'sale'
    ORDER BY {sort_by}
    """
    cursor.execute(query)
    items = cursor.fetchall()
    conn.close()

    # Save to temporary file for easier viewing
    temp_file = "/tmp/sold_items_list.txt"
    with open(temp_file, "w") as f:
        f.write(f"{'CODE':<10} {'TITLE':<22} {'AMOUNT':<15} {'PRICE':<15} {'PROVIDER':<25} {'DATE'}\n")
        f.write("-" * 100 + "\n")
        for item in items:
            f.write(f"{item[0]:<10} | {item[1]:<20} | x{item[2]:<10} | ${item[3]:<10} | {item[4]:<20} | {item[5]:<20}\n")
    
    # Open in chosen editor
    subprocess.call([EDITOR, temp_file])

if __name__ == "__main__":
    sold_list_menu()

