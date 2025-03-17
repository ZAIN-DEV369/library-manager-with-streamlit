import streamlit as st

# Function to load books from a file
# If the file doesn't exist, it initializes an empty file
def load_books():
    books = []
    try:
        with open("library.txt", "r") as f:
            for line in f.readlines():
                parts = line.strip().split(',')
                if len(parts) == 5:
                    title, author, year_str, genre, read_str = parts
                    books.append({
                        'title': title,
                        'author': author,
                        'year': int(year_str),
                        'genre': genre,
                        'read': read_str == 'True'
                    })
    except FileNotFoundError:
        pass
    return books

# Function to save books to a file
def save_books(books):
    with open("library.txt", "w") as f:
        for book in books:
            f.write(f"{book['title']},{book['author']},{book['year']},{book['genre']},{book['read']}\n")

def main():
    st.title("Personal Library Manager")
    
    # Initialize session state for books if not already set
    if 'books' not in st.session_state:
        st.session_state.books = load_books()
    
    # Sidebar menu options
    menu_options = ["Add Book", "Remove Book", "Search", "Display All", "Statistics", "Exit"]
    choice = st.sidebar.radio("Menu", menu_options)
    
    # Adding a new book
    if choice == "Add Book":
        st.subheader("Add a New Book")
        title = st.text_input("Title").strip()
        author = st.text_input("Author").strip()
        year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
        genre = st.text_input("Genre").strip()
        read_status = st.radio("Have you read this book?", ("Yes", "No")) == "Yes"
        
        if st.button("Add Book"):
            st.session_state.books.append({
                'title': title, 'author': author, 'year': year, 'genre': genre, 'read': read_status
            })
            st.success("Book added successfully!")
    
    # Removing a book by title
    elif choice == "Remove Book":
        st.subheader("Remove a Book")
        title_to_remove = st.text_input("Enter the exact title of the book to remove").strip()
        
        if st.button("Remove Book"):
            books_before = len(st.session_state.books)
            st.session_state.books = [book for book in st.session_state.books if book['title'] != title_to_remove]
            
            if len(st.session_state.books) < books_before:
                st.success("Book removed successfully!")
            else:
                st.error("Book not found.")
    
    # Searching for a book by title or author
    elif choice == "Search":
        st.subheader("Search for a Book")
        search_by = st.radio("Search by:", ["Title", "Author"])
        search_term = st.text_input(f"Enter {search_by.lower()} to search for").strip().lower()
        
        if st.button("Search"):
            results = [book for book in st.session_state.books if search_term in book[search_by.lower()].lower()]
            
            if results:
                st.write("### Matching Books:")
                for idx, book in enumerate(results, 1):
                    st.write(f"{idx}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
            else:
                st.write("No books found.")
    
    # Displaying all books in the library
    elif choice == "Display All":
        st.subheader("Your Library")
        
        if st.session_state.books:
            for idx, book in enumerate(st.session_state.books, 1):
                st.write(f"{idx}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.write("Your library is empty.")
    
    # Displaying statistics about the library
    elif choice == "Statistics":
        st.subheader("Library Statistics")
        total_books = len(st.session_state.books)
        
        st.write(f"**Total Books:** {total_books}")
        if total_books > 0:
            read_count = sum(book['read'] for book in st.session_state.books)
            st.write(f"**Percentage Read:** {read_count / total_books * 100:.1f}%")
        else:
            st.write("No statistics available. Add some books first!")
    
    # Exit option - Saves library and exits
    elif choice == "Exit":
        save_books(st.session_state.books)
        st.success("Library saved successfully. Goodbye!")

if __name__ == "__main__":
    main()

 
 st.write("Made BY Zain ul Abideen")
