from click import command
from numpy.core.defchararray import isnumeric


class Phone:
    def __init__(self, phone_id, make, model, price):
        self.__make = make
        self.__model = model
        self.__price = price
        self.__phone_id = phone_id

    def get_make(self):
        return self.__make

    def get_model(self):
        return self.__model

    def get_price(self):
        return self.__price

    def get_id(self):
        return self.__phone_id

    def set_info (self, make, model, price):
        self.__make = make
        self.__model = model
        self.__price = price

    def __str__(self):
        return f"ID: {self.__phone_id} | {self.__make} {self.__model} | Price: ${self.__price}"


inventory = {}
def display_menu():
    print("\nSelect the program (1-5) to run:"
          "\n1. Search for a phone"
          "\n2. Add a new phone"
          "\n3. Update phone details"
          "\n4. Delete a phone"
          "\n5. Display all phone"
          "\n6. Show average price"
          "\n7. Show most expensive phone"
          "\n8. Quit the program")

def add_phone():
    phone_id = input('Enter Phone ID: ')
    if phone_id in inventory:
        print("Phone ID already exists!")
        return
    make = input("Enter make: ")
    model = input("Enter model: ")
    price_input = input("Enter price: ")
    if not price_input.isnumeric():
        print("Price must be a number.")
        return
    price = int(price_input)
    phone = Phone(phone_id, make, model, price)
    inventory[phone_id] = phone
    print("Phone added successfully.")

def search_phone():
    phone_id = input('Enter Phone ID to search: ')
    if phone_id in inventory:
        print(inventory[phone_id])
    else:
        print("Phone not found.")

def update_phone():
    phone_id = input('Enter Phone ID to update: ')
    if phone_id in inventory:
        phone = inventory[phone_id]
        print(f"Current Details: {phone}")
        new_make = input("Enter new make (leave blank to keep current): ")
        new_model = input("Enter new model (leave blank to keep current): ")
        new_price_input = input("Enter new price (leave blank to keep current): ")

        if new_make:
            phone.set_make(new_make)
        if new_model:
            phone.set_model(new_model)
        if new_price_input:
            if new_price_input.isnumeric():
                phone.set_price(int(new_price_input))
            else:
                print("Invalid price entered. Keeping previous price.")
        print("Phone details updated.")
    else:
        print("Phone not found.")

def delete_phone():
    phone_id = input('Enter Phone ID to delete: ')
    if phone_id in inventory:
        del inventory[phone_id]
        print("Phone deleted.")
    else:
        print("Phone not found.")

def display_all_phones():
    if not inventory:
        print("Inventory is empty.")
    else:
        print("\n--- All Phones ---")
        for phone in inventory.values():
            print(phone)
def avg_price():
    if not inventory:
        print("Inventory is empty.")
    else:
        print(f"Average price of all phones: ${sum(phone.get_price() for phone in inventory.values()) / len(inventory)}")
#
# def avg_price():
#     if not inventory:
#         print("Inventory is empty.")
#     else:
#         total = sum(phone.get_price() for phone in inventory.values())
#         average = total / len(inventory)
#         print(f"Average price of all phones: ${average:.2f}")

# --- Main Program ---
def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            search_phone()
        elif choice == '2':
            add_phone()
        elif choice == '3':
            update_phone()
        elif choice == '4':
            delete_phone()
        elif choice == '5':
            display_all_phones()
        elif choice == '6':
            avg_price()
        # elif choice == '7':
        #     most_exp_ph()
        elif choice == '8':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 6.")

print(main())


