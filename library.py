
import math
from book import Book

class Library:
    def __init__(self, library_id, books, total_books, books_in_parallel, time):
        self.id = library_id
        self.books = books.sort(key=lambda x: x.punctuation, reverse=True)
        self.total_books = total_books
        self.books_in_parallel = books_in_parallel
        self.time = time

    def get_punctuation(self, availible_time, scanned_books):
        punctuation = 0
        for i in math.ceil(int(len(self.books)/self.books_in_parallel)):
            if(i==availible_time):
                break
            position = i*self.books_in_parallel
            if position+self.books_in_parallel < len(books):
                punctuation = puctuation + self.sum_punctuations(self.books[position], scanned_books)
        return punctuation

    def sum_punctuations(self, books, scanned_books):
        puctuation = 0
        books = list(set(books)-set(scanned_books))
        for book in books:
            puctuation = puntuation + book.punctuation
        return punctuation