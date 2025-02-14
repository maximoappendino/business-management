import os
from database import Database

db = Database()

def add_provider():
    """Adds a new provider to the database."""
    new_provider = input("Enter new provider name: ").strip()
    if not new_provider:
        print("Invalid name. Operation canceled.")
        return

    db.execute_query("INSERT INTO providers (name) VALUES (?)", (new_provider,))
    print(f"Provider '{new_provider}' added successfully!")

# Path to providers file
providers_path = os.path.join(os.path.dirname(__file__), 'data', 'providers.txt')

def list_providers():
    """Lists all providers from the database."""
    providers = db.fetch_all("SELECT name FROM providers")  # Retrieve providers from the database
    if not providers:
        print("No providers found.")
        return []

    for idx, provider in enumerate(providers, 1):
        print(f"{idx}. {provider[0]}")  # provider[0] because query returns a list of tuples

    return [provider[0] for provider in providers]  # Return a list of provider names


## Path to providers file
#providers_path = os.path.join(os.path.dirname(__file__), 'data', 'providers.txt')

# def list_providers():
#     """Lists all providers."""
#     if not os.path.exists(providers_path):
#         print("No providers found.")
#         return []
#     with open(providers_path, 'r') as file:
#         providers = file.readlines()
#     providers = [p.strip() for p in providers if p.strip()]
#     for idx, provider in enumerate(providers, 1):
#         print(f"{idx}. {provider}")
#     return providers

#def add_provider():
#    """Adds a new provider."""
#    new_provider = input("Enter new provider name: ").strip()
#    if not new_provider:
#        print("Invalid name. Operation canceled.")
#        return
#    with open(providers_path, 'a') as file:
#        file.write(new_provider + '\n')
#    print(f"Provider '{new_provider}' added successfully!")

def settings_menu():
    while True:
        print("\nSETTINGS")
        print("1. List providers")
        print("2. Add provider")
        print("Q. Quit")
        choice = input("Select an option: ").strip().lower()
        if choice == '1':
            list_providers()
        elif choice == '2':
            add_provider()
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    settings_menu()

