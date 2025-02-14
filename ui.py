import os
import time
# from utils import clear_screen, print_colored
from utils import validate_positive_number, validate_code_format, format_currency, clear_screen, print_colored

def display_main_menu(logs):
    """Displays the main menu with options and recent logs."""
    clear_screen()
    print_colored("\nINVENTORY MANAGEMENT SYSTEM", "cyan")
    print_colored("=================================", "yellow")
    print_colored("Recent Activity:", "green")
    for log in logs[-5:]:  # Show last 5 log entries
        print_colored(log.strip(), "white")
    print_colored("=================================", "yellow")
    print_colored("1. Add Item", "blue")
    print_colored("2. Delete Item", "blue")
    print_colored("3. Edit Item", "blue")
    print_colored("4. Search Item", "blue")
    print_colored("5. View List", "blue")
    print_colored("6. View Graph", "blue")
    print_colored("7. Settings", "blue")
    print_colored("8. Sold items", "blue")
    print_colored("Q. Quit", "red")

def get_user_choice():
    """Gets user choice for the main menu."""
    choice = input("\nEnter your choice: ").strip().lower()
    return choice

def load_logs(log_file):
    """Loads recent logs from the log file."""
    if not os.path.exists(log_file):
        return []
    with open(log_file, "r") as f:
        return f.readlines()

def main_ui():
    """Main UI loop for the application."""
    log_file = os.path.join(os.path.dirname(__file__), "data", "log.txt")
    while True:
        logs = load_logs(log_file)
        display_main_menu(logs)
        choice = get_user_choice()
        
        if choice == '1':
            import add
            add.add_item()
        elif choice == '2':
            import remove
#            remove.delete_item()
            remove.remove_item()
        elif choice == '3':
            import edit
            edit.edit_item()
        elif choice == '4':
            import search
            search.search_menu()
        elif choice == '5':
            import list
            list.list_menu()
        elif choice == '6':
            import graphing
            graphing.graphing_menu()
        elif choice == '7':
            import settings
            settings.settings_menu()
        elif choice == '8':
            import sold
            sold.sold_list_menu()
        elif choice == 'q':
            print_colored("Exiting...", "red")
            time.sleep(1)
            break
        else:
            print_colored("Invalid option. Please try again.", "red")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_ui()

