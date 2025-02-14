import sqlite3
import os
from database import Database

# Path to log file
log_path = os.path.join(os.path.dirname(__file__), 'data', 'log.txt')

def log_operation(entry):
    """Logs operations to log.txt"""
    with open(log_path, 'a') as log_file:
        log_file.write(entry + '\n')

def edit_item():
    db = Database()
    
    code = input("Enter item code to edit: ").strip()
    if not code:
        print("Invalid code. Operation canceled.")
        return
    
    existing_item = db.fetch_one("SELECT code, title, provider FROM inventory WHERE code = ?", (code,))
    if not existing_item:
        print("Item not found. Operation canceled.")
        return
    
    new_code = input(f"Enter new code ({existing_item[0]} to keep): ").strip() or existing_item[0]
    new_title = input(f"Enter new title ({existing_item[1]} to keep): ").strip() or existing_item[1]   
    new_provider = input(f"Enter new provider ({existing_item[2]} to keep): ").strip() or existing_item[2]
    
    db.execute_query("UPDATE inventory SET code = ?, title = ?, provider = ?, last_updated = CURRENT_TIMESTAMP WHERE code = ?", 
                     (new_code, new_title, new_provider, code))
    
    log_operation(f"Edited: {code} -> {new_code}, {new_title}, {new_provider}")
    
    db.close()
    print("Item edited successfully!")

if __name__ == "__main__":
    edit_item()

