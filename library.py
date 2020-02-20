import xrange
import math

class Library:
    def __init__(self, library_id, books, books_in_parallel, time):
        self.id = library_id
        self.books = books.sort()
        self.books_in_parallel = books_in_parallel
        self.time = time

    def get_punctuation(availible_time, scanned_books):
        punctuation = 0
        for i in math.ceil(int(len(self.books)/self.books_in_parallel)):
            position = i*self.books_in_parallel
            if position+self.books_in_parallel < len(books):
                puntuation = puctuation + self.sum_punctuations(self.books[position])

def main():

if __name__ == "__main__":
    main()