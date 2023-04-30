from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sqlite3

connection = sqlite3.connect('menu_and_tables.db')
cursor = connection.cursor()

# Notifying the server owner that the server has started
print("Server started")

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
        
    
    def get_available_table_list():
        """Get table list from database"""
        print("Client requested table list")
        
        table_list = cursor.execute('SELECT * FROM tables').fetchall()
        
        available_tables = []
        for table in table_list:
            if table[1] == "Available":
                available_tables.append(table[0])
        
        return available_tables
   
    server.register_function(get_available_table_list, "get_available_table_list")
    
    
    def reserve_table(table_id, user_name):
        """Reserve a table"""
        print(f"Client requested to reserve table {table_id}")
        
        cursor.execute('UPDATE tables SET table_status = "Reserved", table_reservation = ? WHERE table_id = ?', (user_name, table_id,))
        connection.commit()
            
        table_status = cursor.execute('SELECT * FROM tables WHERE table_id = ? AND table_reservation = ?', (table_id, user_name,)).fetchall()
            
        return table_status
    
    server.register_function(reserve_table, "reserve_table")
    
    
    def view_single_reservation(user_name):
        """View single reservation"""
        print(f"Client requested to view reservation of {user_name}")
        
        table_status = cursor.execute('SELECT * FROM tables WHERE table_reservation = ?', (user_name,)).fetchall()
        
        return table_status
    
    server.register_function(view_single_reservation, "view_single_reservation")
    
    
    def check_reservation_exists(user_name):
        """Check if reservation exists"""
        
        exists = cursor.execute('SELECT * FROM tables WHERE table_reservation = ?', (user_name,)).fetchall()
        
        if len(exists) == 0:
            return False
        else:
            return True
        
    server.register_function(check_reservation_exists, "check_reservation_exists")
        
        
    def get_menu():
        """Get menu from database"""
        print("Client requested menu")
        
        menu = cursor.execute('SELECT * FROM menu').fetchall()
        
        return menu
    
    server.register_function(get_menu, "get_menu")
    
    
    def make_an_order(user_name, order):
        """Make an order"""
        print("Client requested to make an order for a table")
        
        cursor.execute('UPDATE tables SET table_status = "Ordered", ordered_items = ? WHERE table_reservation = ?', (order, user_name,))
        connection.commit()
        
        table_status = cursor.execute('SELECT * FROM tables WHERE table_reservation = ?', (user_name,)).fetchall()
        
        return table_status
    
    server.register_function(make_an_order, "make_an_order")
        
        
    def process_payment(user_name):
        """Process payment"""
        print("Client requested to process payment")
        
        customer_order = cursor.execute('SELECT ordered_items FROM tables WHERE table_reservation = ?', (user_name,)).fetchall()

        # If the customer has not ordered anything, return False
        if customer_order[0][0] == "-":
            return False
        
        else:
            customer_order = customer_order[0][0].split(";")

            iter_count = 0
            food_query = ""
            
            for item in customer_order:
                if iter_count == 0:
                    food_query += f'food_id = {item}'
                else:
                    food_query = food_query + f' OR food_id = {item}'
                
                iter_count += 1
            
            ordered_items = cursor.execute('SELECT * FROM menu WHERE ' + food_query).fetchall()

            # Update table total income
            total_price = 0
            for item in ordered_items:
                total_price += item[2]
            
            table_total_income = cursor.execute('SELECT total_income FROM tables WHERE table_reservation = ?', (user_name,)).fetchall()
            table_total_income = table_total_income[0][0] + total_price
            
            cursor.execute('UPDATE tables SET table_status = "Available", ordered_items = "-", table_reservation = "No reservation", total_income = ? WHERE table_reservation = ?', (table_total_income, user_name,))
            connection.commit()

            return ordered_items
    
    server.register_function(process_payment, "process_payment")

    def get_total_income():
        """Get total income"""

        total_income = cursor.execute('SELECT table_id, total_income FROM tables').fetchall()
        
        return total_income
    
    server.register_function(get_total_income, "get_total_income")


    def cancel_reservation(user_name):
        """Cancel reservation"""
        print("Client requested to cancel reservation")

        cursor.execute('UPDATE tables SET table_status = "Available", ordered_items = "-", table_reservation = "No reservation" WHERE table_reservation = ?', (user_name,))
        connection.commit()
        
        return True
    
    server.register_function(cancel_reservation, "cancel_reservation")

    def get_table_status():
        """Get status of all tables"""
        
        tables = cursor.execute('SELECT * FROM tables').fetchall()
        
        return tables
    
    server.register_function(get_table_status, "get_table_status")

    def close_open_table(table_id):
        """Close table"""

        table = cursor.execute('SELECT table_status FROM tables WHERE table_id = ?', (table_id,)).fetchall()

        # If table has ordered or it is reserved, admin can't manage table status
        if table[0][0] == "Reserved" or table[0][0] == "Ordered":
            return False
        elif table[0][0] == "Available":
            cursor.execute('UPDATE tables SET table_status = "Closed", ordered_items = "-", table_reservation = "No reservation" WHERE table_id = ?', (table_id,))
            connection.commit()
            return "Closed"
        elif table[0][0] == "Closed":
            cursor.execute('UPDATE tables SET table_status = "Available", ordered_items = "-", table_reservation = "No reservation" WHERE table_id = ?', (table_id,))
            connection.commit()
            return "Available"
        
        # If table status is not one of the above, return error
        return "Error"
    
    server.register_function(close_open_table, "close_open_table")


    # Run the server's main loop
    server.serve_forever()