import xmlrpc.client
from datetime import datetime

server = xmlrpc.client.ServerProxy('http://localhost:8000')
print("Welcome!\n")
print("You are using admin client.")

def main():
    """Main function for the admin client. Responsible for showing the menu and calling the functions"""
    while True:
        # Showing the menu
        print("\n##############\nMenu: ")
        choice = input("1. Make a reservation\n2. Cancel reservation \n3. Close/Open reservations for a table\n4. View Table Total Income\n5. View Table Status \n0. Exit\nEnter your choice: ")

        if choice == "1":
            make_a_reservation()
        elif choice == "2":
            cancel_reservation()
        elif choice == "3":
            close_open_table()
        elif choice == "4":
            view_table_total_income()
        elif choice == "5":
            view_table_status()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
            continue

    print("\n##############\nThank you for visiting us!")
    print("Goodbye!\n")


def make_a_reservation():
    """
    Function for getting the list of tables and making a reservation.
    In case if customer wants to make a reservation by phone call, for example
    """
    customer_name = ask_customer_name()
    
    existing_reservation = server.check_reservation_exists(customer_name)
    
    # If user already has a reservation decline a new reservation
    if existing_reservation == True:
        print("\n##############\Customer already has a reservation.\nCustomer can have one reservation at a time.")
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
            selection = int(input("Enter the table number to reserve (0 - exit): "))
            if selection == 0:
                return
            elif selection not in table_list:
                print("This table is not available. Please try again.")
                continue
            break
        
        reservation_status = server.reserve_table(selection, customer_name)
        customer_name_database = reservation_status[0][2].replace("_", " ")
        
        print(f"\n##############\nTable reserved!\nTable is: {reservation_status[0][0]}\nName is: {customer_name_database}\nReservation time: {datetime.now()}\n")


def cancel_reservation():
    """
    For cancelling the reservation
    In case if customer wants to cancel a reservation by phone call, for example
    """
    customer_name = ask_customer_name()

    reservation_exists = server.check_reservation_exists(customer_name)

    if reservation_exists == False:
        print("\n##############\nCustomer doesn't have a reservation. Please make a reservation first.")
        return False
    
    else:
        cancel = input(f"\n##############\nAre you sure you want to cancel {customer_name} reservation? (y/n): ")

        if cancel == "y":
            server.cancel_reservation(customer_name)
            print("Reservation has been cancelled.")
        else:
            print("Reservation has not been cancelled.")
            return 
    
def close_open_table():
    """Function for making tables unavailable for reservations"""
    view_table_status()

    table_id = int(input("\nTable number to close/open (one table) (0 - exit): "))

    status = server.close_open_table(table_id)
    if status == False:
        print("\nYou can't manage reserved tables!")
    elif status == "Error":
        print("\nSome error ocurred!")
    else:
        print(f"\nTable {table_id} is now {status}")


def view_table_total_income():
    """Function for tracking the total income of all tables"""
    table_total_income = server.get_total_income()

    total_income = 0
    print(f"\n##############\nTotal income for each table:")
    for table_data in table_total_income:
        total_income += table_data[1]
        print(f"Table {table_data[0]}: {table_data[1]}€")
    print("\nThe total income for all tables is: ", total_income,"€")

def view_table_status():
    """Function for tracking the status of all tables"""
    table_status = server.get_table_status()
    print(f"\n##############\nTable status:")
    for table in table_status:
        print(f"Table {table[0]}: {table[1]} ; {table[2]}")

def ask_customer_name():
    customer_name = input("Enter customer name: ")
    customer_name = customer_name.replace(" ", "_")
    return customer_name

main()