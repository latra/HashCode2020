import requests
import re
from localsearch.currentint import Book, Library


class Dataset:
    def __init__(self, URL):
        raw_values = re.split(r'\n', requests.get(URL).text)[:-1]
        dataset_globals = re.split(r'\s', raw_values.pop(0))
        self.total_books = int(dataset_globals.pop(0))
        self.total_libraries = int(dataset_globals.pop(0))
        self.total_days = int(dataset_globals.pop(0))

        self.books = []
        book_id = 0
        for book_value in re.split(r'\s', raw_values.pop(0)):
            self.books.append(Book(book_id, int(book_value)))
            book_id += 1
        self.libraries = []
        for library in range(self.total_libraries):
            library_data = re.split(r'\s', raw_values.pop(0))
            total_books = int(library_data.pop(0))
            time = int(library_data.pop(0))
            parallel = int(library_data.pop(0))

            books = []
            for book in re.split(r'\s', raw_values.pop(0)):
                books.append(self.books[int(book)])
            hash_books = {}
            for book in books:
                hash_books[book.book_id] = book
            self.libraries.append(Library(library, hash_books, time, parallel))
