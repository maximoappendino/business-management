import sqlite3
import os
from database import Database

# Path to log file
log_path = os.path.join(os.path.dirname(__file__), 'data', 'log.txt')

def log_operation(entry):
    """Logs operations to log.txt"""
    with open(log_path, 'a') as log_file:
        log_file.write(entry + '\n')

def add_item():
    db = Database()
    
    # Get item details from user
    code = input("Enter item code: ").strip()
    if not code:
        print("Invalid code. Operation canceled.")
        return
    
    try:

        # Check if the item already exists in the inventory
        existing_item = db.fetch_one("SELECT amount, title FROM inventory WHERE code = ?", (code,))
        if existing_item:
            # Skip title input if item already exists
            print(f"Item with code {code} already exists. Skipping title input.")
            title = existing_item[1]  # Use the existing title
        else:
            title = input("Enter item title: ").strip()
            if not title:
                print("Invalid title. Operation canceled.")
                return

       
        amount = int(input("Enter amount: ").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Invalid amount. Operation canceled.")
        return
  
    
    purchase_price = float(input("Enter purchase price: ").strip())
    if purchase_price < 0:
        print("Invalid price. Operation canceled.")
        return
    
    # Fetch providers
    providers = db.fetch_all("SELECT id, name FROM providers")
    if not providers:
        print("No providers found. Add providers in SETTINGS.")
        return
    
    print("Select a provider:")
    for pid, pname in providers:
        print(f"{pid}. {pname}")
    
    try:
        provider_id = int(input("Enter provider number: ").strip())
        provider = db.fetch_one("SELECT name FROM providers WHERE id = ?", (provider_id,))
        if not provider:
            raise ValueError
    except ValueError:
        print("Invalid provider. Operation canceled.")
        return
    
    provider_name = provider[0]
    
    # Check if item already exists
    existing_item = db.fetch_one("SELECT amount FROM inventory WHERE code = ?", (code,))
    
    if existing_item:
        new_amount = existing_item[0] + amount
        db.execute_query("UPDATE inventory SET amount = ?, purchase_price = ?, provider = ?, last_updated = CURRENT_TIMESTAMP WHERE code = ?", 
                         (new_amount, purchase_price, provider_name, code))
        print("Item updated successfully!")
    else:
        db.execute_query("INSERT INTO inventory (code, title, amount, purchase_price, provider) VALUES (?, ?, ?, ?, ?)",
                 (code, title, amount, purchase_price, provider_name))

#        db.execute_query("INSERT INTO inventory (code, title, amount, purchase_price, provider) VALUES (?, ?, ?, ?, ?)", 
#                         (code, "UNKNOWN", amount, purchase_price, provider_name))
        print("Item added successfully!")
     

    # Log operation
    log_operation(f"Added: {amount}x {code} at ${purchase_price} from {provider_name}")
    
    db.execute_query("INSERT INTO transactions (code, amount, price, transaction_type) VALUES (?, ?, ?, 'purchase')", 
                     (code, amount, purchase_price))
    db.close()

if __name__ == "__main__":
    add_item()

