import requests
import re
from book import Book
from library import Library

class Dataset:
  def __init__(self,URL):
    raw_values = re.split(r'\n',requests.get(URL).text)[:-1]
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
      self.libraries.append(Library(library,books,total_books,parallel,time))

  def solve(self):
    days_left = self.total_days
    libraries = self.libraries
    books_alredy_scanned = []
    points = 0
    number_of_libraries = 0
    best_libraries = []
    while days_left > 0:
      best_library = None
      best_punct = 0
      for library in self.libraries:
        punct = library.get_punctuation2(days_left, books_alredy_scanned)
        if punct > best_punct:
          best_library = library
          best_punct = punct
      days_left -= best_library.signup_time
      books_alredy_scanned += best_library.books
      libraries.pop(libraries.index(best_library))
      points += best_punct
      number_of_libraries += 1
      #print(days_left, best_library.id, points)

    print(number_of_libraries)
    for library in best_libraries:
      print(str(library.id) + " " + str(len(library.good_books)))
      for book in library.good_books:
        print(book.id, end=" ")
