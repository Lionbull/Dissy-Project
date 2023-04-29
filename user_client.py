import xmlrpc.client
from datetime import datetime

server = xmlrpc.client.ServerProxy('http://localhost:8000')

user_name = input("Enter your name: ")
user_name = user_name.replace(" ", "_")

def main():
    """Main function for the client. Responsible for showing the menu and calling the functions"""
    while True:
        # Showing the menu
        print("\n##############\nMenu: ")
        choice = input("1. Make a reservation\n2. Make an order\n3. Pay the order \n4. View my reservation \n5. Cancel reservation \n0. Exit\nEnter your choice: ")

        if choice == "1":
            make_a_reservation()
        elif choice == "2":
            make_an_order()
        elif choice == "3":
            pay_the_order()
        elif choice == "4":
            view_my_reservation()
        elif choice == "5":
            cancel_reservation()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            continue


def make_a_reservation():
    """Function for getting the list of tables and making a reservation"""
    global user_name
    
    existing_reservation = server.check_reservation_exists(user_name)
    
    # If user already has a reservation decline a new reservation
    if existing_reservation == True:
        print("\n##############\nYou already have a reservation.\nUser can have one reservation at a time.")
        return
    
    else:
    
        # Getting the list of tables
        table_list = server.get_available_table_list()
        
        # Showing the list of tables
        print("\n##############\nList of currently available tables:")
        
        for table in table_list:
            print(f"Table {table} is available")
        
        while True:
            # Getting the user input
            selection = int(input("Enter the table number you want to reserve (0 - exit): "))
            if selection == 0:
                return
            elif selection not in table_list:
                print("This table is not available. Please try again.")
                continue
            break
        
        reservation_status = server.reserve_table(selection, user_name)
        user_name_database = reservation_status[0][2].replace("_", " ")
        
        print(f"\n##############\nTable reserved!\n Your table is: {reservation_status[0][0]}\n Your name is: {user_name_database}\n Reservation time: {datetime.now()}\n")


def view_my_reservation():
    """Function for viewing the user's reservation"""
    global user_name
    reservation_exists = server.check_reservation_exists(user_name)
    if reservation_exists == False:
        print("\n##############\nYou don't have a reservation. Please make a reservation first.")
        return
    else:
        reservation_status = server.view_single_reservation(user_name)
        user_name_database = reservation_status[0][2].replace("_", " ")
    
    print(f"\n##############\nYour table is: {reservation_status[0][0]}\nYour name is: {user_name_database}\n")


def make_an_order():
    """For making an order"""
    global user_name
    reservation_exists = server.check_reservation_exists(user_name)
    
    if reservation_exists == False:
        print("You don't have a reservation. Please make a reservation first.")
        return
    else:
        menu = server.get_menu()
        print("\n##############\nMenu:")
        for item in menu:
            print(f"{item[0]}. {item[1]} - {item[2]}")
            
        menu_selection = input("Please, enter the numbers of items (separated by semicolon): ")
              
        order_status = server.make_an_order(user_name, menu_selection)
        
        print(f"\n##############\nYou have made an order! Your order is: {order_status[0][3]}")
        
    
def pay_the_order():
    """For paying the order"""
    global user_name
    
    
    pass


def cancel_reservation():
    """For cancelling the reservation"""
    
    pass
    
    
main()