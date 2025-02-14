import os
import sqlite3
import subprocess

# Configuration
EDITOR = "vim"  # Change to your preferred editor
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "inventory.db")

def list_menu():
    sort_by = {
        "date": "last_updated",
        "price": "purchase_price",
        "amount": "amount",
        "title": "title",
        "provider": "provider"
    }
    """Displays the list menu."""
    while True:
        print("\nLIST MENU")
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
            list_items(sort_by["date"])
        elif choice == '2':
            list_items(sort_by["price"])
        elif choice == '3':
            list_items(sort_by["amount"])
        elif choice == '4':
            list_items(sort_by["title"])
        elif choice == '5':
            list_items(sort_by["provider"])
        else:
            print("Invalid choice. Try again.")
            continue


def list_items(sort_by):
    """Lists items sorted by the given parameter."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor() 
    query = f"SELECT code, title, amount, purchase_price, provider, last_updated FROM inventory ORDER BY {sort_by}"
    cursor.execute(query)
    items = cursor.fetchall()
    conn.close()
    
    # Save to temporary file for easier viewing
    temp_file = "/tmp/inventory_list.txt"
    with open(temp_file, "w") as f:
        f.write(f"{'CODE':<10} {'TITLE':<22} {'AMOUNT':<15} {'PRICE':<15} {'PROVIDER':<25} {'DATE'}\n")
        f.write("-" * 100 + "\n")
        for item in items:
            f.write(f"{item[0]:<10} | {item[1]:<20} | x{item[2]:<10} | ${item[3]:<10} | {item[4]:<20} | {item[5]:<20}\n")
    
    # Open in chosen editor
    subprocess.call([EDITOR, temp_file])

#    # Call the list_items function with the selected sort option and order
#    list_items(sort_by)

if __name__ == "__main__":
    list_menu()

