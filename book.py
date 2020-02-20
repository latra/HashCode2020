#!/usr/bin/python3
class Book:
    def __init__(self, book_id, puntuacion):
        self.book_id = book_id
        self.puntuacion = puntuacion
    def __eq__(self, other):
        return self.puntuacion == other.puntuacion
    def __lt__(self, other):
        return self.puntuacion < other.puntuacion
    def __gt__(self, other):
        return self.puntuacion > other.puntuacion
    def __le__(self, other):
        return self.puntuacion <= other.puntuacion
    def __ge__(self, other):
        return self.puntuacion >= other.puntuacion