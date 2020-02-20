#!/usr/bin/python3
from book import Book
from library import Library

book0 = Book("0", "1")
book1 = Book(1, 2)
book2 = Book(2, 3)
book3 = Book(3, 6)
book4 = Book(4, 5)
book5 = Book(5, 4)

library0 = Library(0, [ book0, book1, book2, book3, book4 ], 5, 2, 2)
library1 = Library(1, [ book3, book2, book5, book0 ],4,1, 3)
def testValues(actual, expected):
    if (actual == expected):
        print('OK')
    else:
        print('KO: ' + str(actual) + '!=' + str(expected))

def libraryTests():
    print(library0.books)
    print(library0.get_punctuation(1000,[]))

def bookTests():

    testValues(book0 < book2, True)
    testValues(book0 > book2, False)
    testValues(book3 > book4, True)
    testValues(book1 > book2, False)

def main():
    bookTests()
    libraryTests()


if __name__ == "__main__":
    main()