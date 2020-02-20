
import math
from book import Book

class Library:
    def __init__(self, library_id, books, total_books, books_in_parallel, time):
        self.id = int(library_id)
        self.books = int(books)
        self.books.sort(key=lambda x: x.punctuation, reverse=True)
        self.total_books = int(total_books)
        self.books_in_parallel = int(books_in_parallel)
        self.time = int(time)

    def print_books(self):
        for book in self.books:
            print(f"Ordered books: {book}")

    def get_punctuation(self, availible_time, scanned_books):
        punctuation = 0
        for i in range (math.ceil(int(len(self.books)/self.books_in_parallel))):
            if(i==availible_time):
                break
            position = i*self.books_in_parallel
            if position+self.books_in_parallel < len(self.books):
                punctuation = punctuation + self.sum_punctuations(self.books[position:position+self.books_in_parallel], scanned_books)
        return punctuation

    def sum_punctuations(self, books, scanned_books):
        punctuation = 0
        books = list(set(books)-set(scanned_books))
        for book in books:
            punctuation = punctuation + book.punctuation
        return punctuation