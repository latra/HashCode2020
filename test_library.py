from library import Library
from book import Book

def main():
    library = Library(1, [Book(0, 3), Book(1,5)],2, 1, 2)
    library.print_books()
    pass

if __name__ == "__main__":
    main()