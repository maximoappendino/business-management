import os
import sqlite3
from database import Database


# Path to log file
log_path = os.path.join(os.path.dirname(__file__), 'data', 'log.txt')

def log_operation(entry):
    """Logs operations to log.txt"""
    with open(log_path, 'a') as log_file:
        log_file.write(entry + '\n')

def remove_item():
    db = Database()

    # Get the item code and amount to remove
    code = input("Enter item code: ").strip()
    amount_to_remove = int(input("Enter amount to remove: ").strip())

    # Fetch the item details from the inventory
    item = db.fetch_one("SELECT code, title, amount, purchase_price, provider, price FROM inventory WHERE code = ?", (code,))
    
    if not item:
        print("Item not found.")
        return

    # Check if there's enough stock to remove
    current_amount = item[2]
    if current_amount < amount_to_remove:
        print("Not enough stock. Operation canceled.")
        return

    # Get the reason for removal (sold or broken)
    removal_reason = input("Was the item BROKEN? [B] for Broken: ").strip().upper()
    if removal_reason == 'B':
        transaction_label = "broken"
    else:
        transaction_label = "sale"

    try:
        price = float(input("Enter price per unit: ").strip())
        if price < 0:
            raise ValueError
    except ValueError:
        print("Invalid price. Operation canceled.")
        return

    # Remove the item from the inventory (decrease the amount)
    new_amount = current_amount - amount_to_remove
    db.execute_query("UPDATE inventory SET amount = ? WHERE code = ?", (new_amount, code))

    # Log operation
    log_operation(f"Removed: {amount_to_remove}x {item[0]} ({transaction_label}) at ${price}")

    # Insert the removed item into the removed_items table
    db.execute_query("INSERT INTO removed_items (code, title, amount, purchase_price, provider, price, removal_reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (item[0], item[1], amount_to_remove, item[3], item[4], price, transaction_label))

    db.close()
    print("Item removed and moved to removed items.")


#def remove_item():
#    db = Database()
#
#    # Get the item code and amount to remove
#    code = input("Enter item code: ").strip()
#    amount_to_remove = int(input("Enter amount to remove: ").strip())
#
#    # Fetch the item details from the inventory
#    item = db.fetch_one("SELECT code, title, amount, purchase_price, provider, price FROM inventory WHERE code = ?", (code,))
#    
#    if not item:
#        print("Item not found.")
#        return
#
#    # Check if there's enough stock to remove
#    current_amount = item[2]
#    if current_amount < amount_to_remove:
#        print("Not enough stock. Operation canceled.")
#        return
#
#    # Get the reason for removal (sold or broken)
#    removal_reason = input("Was the item BROKEN? [B] for Broken: ").strip().upper()
#    if removal_reason == 'B':
#        transaction_label = "broken"
#    else:
#        transaction_label = "sale"
##        print("Invalid option. Operation canceled.")
##        return
#    try:
#        price = float(input("Enter price per unit: ").strip())
#        if price < 0:
#            raise ValueError
#    except ValueError:
#        print("Invalid price. Operation canceled.")
#        return
#
#
#    # Remove the item from the inventory (decrease the amount)
#    new_amount = current_amount - amount_to_remove
#    db.execute_query("UPDATE inventory SET amount = ? WHERE code = ?", (new_amount, code))
# 
#    # Log operation
##    trabsaction_label = "broken" if transaction_type == 'B' else "sale"
#    log_operation(f"Removed: {amount_to_remove}x {item[0]} ({removal_reason.lower()}) at ${item[5]}")
#
#   
#    # Insert the removed item into the removed_items table
#    db.execute_query("INSERT INTO removed_items (code, title, amount, purchase_price, provider, price, removal_reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                     (item[0], item[1], amount_to_remove, item[3], item[4], item[5], removal_reason))
#
#       db.close()
#    print("Item removed and moved to removed items.")
#
