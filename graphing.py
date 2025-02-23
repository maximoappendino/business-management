import os
import sqlite3
import matplotlib.pyplot as plt

db_path = os.path.join(os.path.dirname(__file__), "data", "inventory.db")

def fetch_sales_data(provider_filter=None, year=None, month=None, price_type="purchase_price"):
    """Fetch sales or purchase data from the database based on filters."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = f"""
    SELECT strftime('%Y-%m', date) AS period, SUM({price_type} * amount) AS total
    FROM history
    WHERE 1 = 1
    """
    params = []
    
    if provider_filter:
        query += " AND provider = ?"
        params.append(provider_filter)
    if year:
        query += " AND strftime('%Y', date) = ?"
        params.append(str(year))
    if month:
        query += " AND strftime('%m', date) = ?"
        params.append(f"{int(month):02d}")
    
    query += " GROUP BY period ORDER BY period"
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    # Fetch data from removed items for the same period
    query_removed = f"""
    SELECT strftime('%Y-%m', removal_date) AS period, SUM(price * amount) AS total
    FROM removed_items
    WHERE 1 = 1
    """
    
    cursor.execute(query_removed, params)
    removed_data = cursor.fetchall()

    # Combine both inventory and removed data
    combined_data = data + removed_data
    
    conn.close()
    
    return combined_data

def plot_graph(data, title):
    """Plot a graph based on the provided data."""
    if not data:
        print("No data available for the selected filters.")
        return
    
    periods, totals = zip(*data)
    
    plt.figure(figsize=(10, 5))
    plt.plot(periods, totals, marker='o', linestyle='-')
    plt.xlabel("Time Period")
    plt.ylabel("Total Value")
    plt.title(title)
    plt.grid()
    plt.xticks(rotation=45)
    plt.show()

def graphing_menu():
    """User interface for selecting graphing options."""
    print("\nGRAPHING MENU")
    price_type = "purchase_price" if input("Graph Purchase Price? (y/n): ").strip().lower() == 'y' else "sale_price"
    provider = input("Enter provider name or leave blank for all: ").strip()
    year = input("Enter year (YYYY) or leave blank for all: ").strip()
    month = input("Enter month (MM) or leave blank for all: ").strip()
    
    data = fetch_sales_data(provider_filter=provider if provider else None,
                            year=year if year else None,
                            month=month if month else None,
                            price_type=price_type)
    
    plot_graph(data, f"{price_type.capitalize()} Trends")

if __name__ == "__main__":
    graphing_menu()

