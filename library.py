
import math
from book import Book

class Library:
    def __init__(self, library_id, books, total_books, books_in_parallel, time):
        self.id = int(library_id)
        self.books = books
        self.books.sort(key=lambda x: x.punctuation, reverse=True)
        self.total_books = int(total_books)
        self.books_in_parallel = int(books_in_parallel)
        self.signup_time = int(time)
        self.good_books = []

    def print_books(self):
        for book in self.books:
            print(book)

    def get_punctuation(self, availible_time, scanned_books):
        punctuation = 0
        availible_time = availible_time-self.signup_time
        for i in range(min(availible_time, math.ceil(int(len(self.books)/self.books_in_parallel)))):
            position = i*self.books_in_parallel
            if position+self.books_in_parallel < len(self.books):
                punctuation = punctuation + \
                    self.sum_punctuations(self.books[position:position+self.books_in_parallel], scanned_books)
            else:
                punctuation = punctuation + self.sum_punctuations(self.books[position:], scanned_books)
        return punctuation

    def get_punctuation2(self, available_time, scanned_books):
        punctuation = 0
        available_time = available_time-self.signup_time
        books = list(set(self.books)-set(scanned_books))
        good_books = list(set(self.books)-set(scanned_books)) 
        self.good_books = []
        for actual_book in self.books:
            if available_time == 0:
                break
            if actual_book in good_books:
                punctuation += actual_book.punctuation
                self.good_books.append(actual_book)
            available_time -= 1
        return punctuation

    def sum_punctuations(self, books, scanned_books):
        punctuation = 0
        books = list(set(books)-set(scanned_books))
        self.good_books += books
        for book in books:
            punctuation = punctuation + book.punctuation
        return punctuation