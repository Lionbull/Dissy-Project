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

            cursor.execute('UPDATE tables SET table_status = "Available", ordered_items = "-", table_reservation = "No reservation" WHERE table_reservation = ?', (user_name,))
            connection.commit()

            return ordered_items
    
    server.register_function(process_payment, "process_payment")


    def cancel_reservation(user_name):
        """Cancel reservation"""
        print("Client requested to cancel reservation")
        
        cursor.execute('UPDATE tables SET table_status = "Available", ordered_items = "-", table_reservation = "No reservation" WHERE table_reservation = ?', (user_name,))
        connection.commit()
        
        return True
    
    server.register_function(cancel_reservation, "cancel_reservation")

    
    # Run the server's main loop
    server.serve_forever()