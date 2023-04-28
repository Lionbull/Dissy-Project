import xmlrpc.client
from datetime import datetime

server = xmlrpc.client.ServerProxy('http://localhost:8000')

def main():
    """Main function for the client. Responsible for showing the menu and calling the functions"""
    while True:
        # Showing the menu
        print("\nMenu: ")
        choice = input("1. Add/Edit topic\n2. Get content of a topic\n3. Search for data in Wikipedia\nEnter your choice: ")

        if choice == "1":
            add_edit_topic()
        elif choice == "2":
            get_content_of_topic()
        elif choice == "3":
            search_wikipedia()
        else:
            print("Invalid choice. Please try again.")
            continue


def example():
    """Function for getting the topic content"""

    # Getting the topic from the user
    example = input("\nEnter the topic: ")

    topic_content = server.example(example)

    
main()