import requests
import re
from book import Book

class Dataset:
  def __init__(self,URL):
    raw_values = re.split(r'\n',requests.get(URL).text)[:-1]
    print(raw_values)
    dataset_globals = re.split(r'\s', raw_values.pop(0))
    print(dataset_globals)
    total_books = dataset_globals.pop(0)
    total_libraries = dataset_globals.pop(0)
    total_days = dataset_globals.pop(0)

    book_values = []
    book_id = 0
    for book_value in re.split(r'\s', raw_values.pop(0)):
        book_values.append(Book(book_id, book_value))
        book_id += 1
    print(book_values)