import streamlit as st
import csv

class Library:
    def __init__(self, path):
        self.path = path
        self.books = self.load_books()

    def load_books(self):
        books = []
        with open(self.path, 'r') as data:
            reader = csv.DictReader(data)
            for row in reader:
                books.append(row)
        return books

    def save_books(self):
        with open(self.path, 'w', newline='') as data:
            colnames = ['bid', 'title', 'author', 'category', 'status']
            writer = csv.DictWriter(data, fieldnames=colnames)
            writer.writeheader()
            for book in self.books:
                writer.writerow(book)

    def add_book(self, bid, title, author, category, status='Available'):
        for book in self.books:
            if book['title'].lower() == title.lower() and book['author'].lower() == author.lower():
                st.error(f'Book {title} by {author} already exists in the library')
                return
        new_book = {
            'bid': bid,
            'title': title,
            'author': author,
            'category': category,
            'status': status
        }
        self.books.append(new_book)
        self.save_books()
        st.success(f"Book '{title}' added successfully.")

    def search_book(self, title):
        for book in self.books:
            if book['title'].lower() == title.lower():
                return book
        return None

    def remove_book(self, title):
        book = self.search_book(title)
        if book:
            self.books.remove(book)
            self.save_books()
            st.success(f"Book '{title}' has been removed from the library.")
        else:
            st.error(f"Book '{title}' is not available in the library.")

    def borrow_book(self, title):
        book = self.search_book(title)
        if book:
            if book['status'].lower() == 'available':
                book['status'] = 'Issued'
                self.save_books()
                st.success(f"Book '{title}' has been issued.")
            else:
                st.warning(f"Book '{title}' is currently not available.")
        else:
            st.error(f"Book '{title}' is not available in the library.")

    def return_book(self, title):
        book = self.search_book(title)
        if book:
            if book['status'].lower() == 'issued':
                book['status'] = 'Available'
                self.save_books()
                st.success(f"Book '{title}' has been returned and is now available.")
            else:
                st.warning(f"Book '{title}' is already available.")
        else:
            st.error(f"Book '{title}' is not available in the library.")

    def display_books(self):
        st.write("Current list of books in the library:")
        for book in self.books:
            st.write(f"ID: {book['bid']}, Title: {book['title']}, Author: {book['author']}, "
                     f"Category: {book['category']}, Status: {book['status']}")

    def search_and_display_book(self, title):
        book = self.search_book(title)
        if book:
            st.write(f"Book found:\nID: {book['bid']}, Title: {book['title']}, Author: {book['author']}, "
                     f"Category: {book['category']}, Status: {book['status']}")
        else:
            st.error(f"Book '{title}' is not available in the library.")

def main():
    st.title("Library Management System")
    library = Library(r"C:\Users\HP\OneDrive\Documents\Books_data_project.csv")

    menu = ["Add Book", "Borrow Book", "Return Book", "Display Books", "Search Book", "Remove Book", "Exit"]
    choice = st.sidebar.selectbox("Select an Option", menu)

    if choice == "Add Book":
        st.subheader("Add a New Book")
        bid = st.text_input("Enter book ID")
        title = st.text_input("Enter book title")
        author = st.text_input("Enter book author")
        category = st.text_input("Enter book category")
        if st.button("Add Book"):
            library.add_book(bid, title, author, category)

    elif choice == "Borrow Book":
        st.subheader("Borrow a Book")
        title = st.text_input("Enter book title to borrow")
        if st.button("Borrow Book"):
            library.borrow_book(title)

    elif choice == "Return Book":
        st.subheader("Return a Book")
        title = st.text_input("Enter book title to return")
        if st.button("Return Book"):
            library.return_book(title)

    elif choice == "Display Books":
        st.subheader("List of Books")
        library.display_books()

    elif choice == "Search Book":
        st.subheader("Search for a Book")
        title = st.text_input("Enter book title to search")
        if st.button("Search Book"):
            library.search_and_display_book(title)

    elif choice == "Remove Book":
        st.subheader("Remove a Book")
        title = st.text_input("Enter book title to remove")
        if st.button("Remove Book"):
            library.remove_book(title)

    elif choice == "Exit":
        st.stop()

if __name__ == "__main__":
    main()
