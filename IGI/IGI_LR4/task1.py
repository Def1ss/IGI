"""
Task 1: Library catalog with CSV and Pickle serialization
"""

import csv
import pickle
import tabulate


class Book:
    def __init__(self, title, author, year, isbn, copies=1):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.copies = copies

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year}) - {self.copies} copies"


class LibraryCatalog:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_by_author(self, author):
        return [b for b in self.books if author.lower() in b.author.lower()]

    def save_csv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'author', 'year', 'isbn', 'copies'])
            for b in self.books:
                writer.writerow([b.title, b.author, b.year, b.isbn, b.copies])
        print(f"Saved to {filename}")

    def load_csv(self, filename):
        self.books = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.books.append(Book(row['title'], row['author'], int(row['year']), row['isbn'], int(row['copies'])))
        print(f"Loaded {len(self.books)} books from {filename}")

    def save_pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.books, f)
        print(f"Saved to {filename}")

    def load_pickle(self, filename):
        with open(filename, 'rb') as f:
            self.books = pickle.load(f)
        print(f"Loaded {len(self.books)} books from {filename}")

    def display_table(self):
        """Display books as a nice table"""
        if not self.books:
            print("No books in catalog")
            return
        table_data = [[b.title, b.author, b.year, b.isbn, b.copies] for b in self.books]
        headers = ["Title", "Author", "Year", "ISBN", "Copies"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


def run():
    print("\n=== TASK 1: LIBRARY CATALOG ===")

    catalog = LibraryCatalog()

    # Sample data
    samples = [
        Book("1984", "George Orwell", 1949, "123", 3),
        Book("Animal Farm", "George Orwell", 1945, "456", 2),
        Book("Pride and Prejudice", "Jane Austen", 1813, "789", 1),
    ]
    for b in samples:
        catalog.add_book(b)

    print("\nCurrent catalog:")
    catalog.display_table()

    # Search
    author = input("\nEnter author name to search: ")
    results = catalog.search_by_author(author)
    if results:
        print(f"\nBooks by {author}:")
        for b in results:
            print(f"  - {b}")
    else:
        print(f"No books found by {author}")

    # Serialization demo
    fmt = input("\nSave to (csv/pickle): ")
    if fmt == "csv":
        catalog.save_csv("library.csv")
        new_cat = LibraryCatalog()
        new_cat.load_csv("library.csv")
        print("\nLoaded catalog:")
        new_cat.display_table()
    elif fmt == "pickle":
        catalog.save_pickle("library.pkl")
        new_cat = LibraryCatalog()
        new_cat.load_pickle("library.pkl")
        print("\nLoaded catalog:")
        new_cat.display_table()