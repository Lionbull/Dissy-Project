import sqlite3

connection = sqlite3.connect('menu_and_tables.db')

cursor = connection.cursor()


# Create table for menu
cursor.execute('''DROP TABLE IF EXISTS menu''')
cursor.execute('''CREATE TABLE menu(food_id INTEGER PRIMARY KEY AUTOINCREMENT, food_name TEXT, food_price INTEGER, food_type TEXT)''')

cursor.execute('''INSERT INTO menu(food_name, food_price, food_type) VALUES("Bread with Salsa", 20, "L")''')
cursor.execute('''INSERT INTO menu(food_name, food_price, food_type) VALUES("Salad", 50, "L")''')
cursor.execute('''INSERT INTO menu(food_name, food_price, food_type) VALUES("Chicken with Rice", 100, "G, L")''')
cursor.execute('''INSERT INTO menu(food_name, food_price, food_type) VALUES("Beef with Potatoes", 200, "G, L")''')

# Create table for tables
cursor.execute('''DROP TABLE IF EXISTS tables''')
cursor.execute('''CREATE TABLE tables(table_id INTEGER PRIMARY KEY AUTOINCREMENT, table_status TEXT, table_reservation TEXT, ordered_items TEXT)''')

cursor.execute('''INSERT INTO tables(table_status, table_reservation, ordered_items) VALUES("Available", "No reservation", "-")''')
cursor.execute('''INSERT INTO tables(table_status, table_reservation, ordered_items) VALUES("Available", "No reservation", "-")''')
cursor.execute('''INSERT INTO tables(table_status, table_reservation, ordered_items) VALUES("Available", "No reservation", "-")''')
cursor.execute('''INSERT INTO tables(table_status, table_reservation, ordered_items) VALUES("Available", "No reservation", "-")''')

connection.commit()

menu_results = cursor.execute('''SELECT * FROM menu''')
results = cursor.fetchall()
print(f"Menu: {results}")

table_results = cursor.execute('''SELECT * FROM tables''')
results = cursor.fetchall()
print(f"Tables: {results}")

connection.close()