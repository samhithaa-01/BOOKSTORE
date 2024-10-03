import pickle
from prettytable import PrettyTable
import sqlite3

class Book:
    def __init__(self, title, author, isbn, price, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Book({self.title}, {self.author}, {self.isbn}, {self.price}, {self.quantity})"


class Bookstore:
    def __init__(self):
        self.inventory = []

    def add_book(self, book):
        self.inventory.append(book)
        print(f"\tAdded '{book.title}' to the inventory.")

    def find_books(self, title):
        """Helper function to find books by title (case insensitive)."""
        return [book for book in self.inventory if title.lower() in book.title.lower()]

    def view_inventory(self):
        if not self.inventory:
            print("\tInventory is empty.")
        else:
            self.print_inventory_table()

    def search_book(self, title):
        found_books = self.find_books(title)
        if found_books:
            print(f"\tFound {len(found_books)} book(s) matching '{title}':")
            self.print_inventory_table(found_books)
        else:
            print(f"\tNo books found with '{title}' in the title.")

    def edit_book(self, title):
        found_books = self.find_books(title)
        if found_books:
            self.print_inventory_table(found_books)
            try:
                book_index = int(input("\tEnter the number of the book to edit: ")) - 1
                if 0 <= book_index < len(found_books):
                    book = found_books[book_index]
                    new_quantity = int(input("\tEnter new quantity: "))
                    book.quantity = new_quantity
                    print(f"\tUpdated quantity for '{book.title}' to {new_quantity}.")
                else:
                    print("\tInvalid book number.")
            except ValueError:
                print("\tInvalid input. Please enter a valid number.")
        else:
            print(f"\tNo books found with '{title}' in the title.")

    def delete_book(self, title):
        found_books = self.find_books(title)
        if found_books:
            self.print_inventory_table(found_books)
            try:
                book_index = int(input("\tEnter the number of the book to delete: ")) - 1
                if 0 <= book_index < len(found_books):
                    deleted_book = self.inventory.pop(self.inventory.index(found_books[book_index]))
                    print(f"\tDeleted '{deleted_book.title}' from the inventory.")
                else:
                    print("\tInvalid book number.")
            except ValueError:
                print("\tInvalid input. Please enter a valid number.")
        else:
            print(f"\tNo books found with '{title}' in the title.")

    def print_inventory_table(self, books=None):
        """Helper function to print a formatted table of books."""
        if books is None:
            books = self.inventory
        if not books:
            print("\tInventory is empty.")
        else:
            table = PrettyTable()
            table.field_names = ["#", "Title", "Author", "ISBN", "Price", "Quantity"]
            for idx, book in enumerate(books, start=1):
                table.add_row([idx, book.title, book.author, book.isbn, f"${book.price}", book.quantity])
            print(table)


class FileHandler:
    @staticmethod
    def save_inventory_to_file(filename, inventory):
        with open(filename, 'wb') as file:
            pickle.dump(inventory, file)

    @staticmethod
    def load_inventory_from_file(filename):
        try:
            with open(filename, 'rb') as file:
                inventory = pickle.load(file)
            return inventory
        except (FileNotFoundError, EOFError):
            return []


class BookstoreManager:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        self.bookstore = Bookstore()

    def load_inventory(self):
        self.bookstore.inventory = FileHandler.load_inventory_from_file(self.inventory_file)
        print(f"\tInventory loaded from '{self.inventory_file}'.")

    def save_inventory(self):
        FileHandler.save_inventory_to_file(self.inventory_file, self.bookstore.inventory)
        print(f"\tInventory saved to '{self.inventory_file}'.")


def get_user_input_for_book():
    """Helper function to get book details from the user."""
    title = input("\tEnter book title: ")
    author = input("\tEnter author: ")
    isbn = input("\tEnter ISBN: ")
    price = float(input("\tEnter price: "))
    quantity = int(input("\tEnter quantity: "))
    return Book(title, author, isbn, price, quantity)


def main():
    inventory_file = "inventory.pkl"
    manager = BookstoreManager(inventory_file)

    actions = {
        "1": ("Add a book to the inventory", lambda: manager.bookstore.add_book(get_user_input_for_book())),
        "2": ("View inventory", manager.bookstore.view_inventory),
        "3": ("Search for a book by title", lambda: manager.bookstore.search_book(input("\tEnter the title to search for: "))),
        "4": ("Edit a book", lambda: manager.bookstore.edit_book(input("\tEnter the title of the book to edit: "))),
        "5": ("Delete a book", lambda: manager.bookstore.delete_book(input("\tEnter the title of the book to delete: "))),
        "6": ("Load inventory from file", manager.load_inventory),
        "7": ("Save inventory to file", manager.save_inventory),
        "8": ("Quit", lambda: print("\tGoodbye!")),
    }

    while True:
        print("\n\t-----------------------------------------")
        print("\t Bookstore Inventory Management System")
        print("\t-----------------------------------------")
        for key, (desc, _) in actions.items():
            print(f"\t {key}. {desc}")
        print("\t-----------------------------------------")

        choice = input("\t Enter your choice: ").strip()

        if choice in actions:
            action = actions[choice][1]
            action()
            if choice == "8":  # Quit
                break
        else:
            print("\tInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
