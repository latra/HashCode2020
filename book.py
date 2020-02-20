#!/usr/bin/python3
class Book:
    def __init__(self, book_id, punctuation):
        self.book_id = book_id
        self.punctuation = punctuation
    def __eq__(self, other):
        return self.punctuation == other.punctuation
    def __lt__(self, other):
        return self.punctuation < other.punctuation
    def __gt__(self, other):
        return self.punctuation > other.punctuation
    def __le__(self, other):
        return self.punctuation <= other.punctuation
    def __ge__(self, other):
        return self.punctuation >= other.punctuation
    def __str__ (self):
        return [self.book_id, self.punctuation]
