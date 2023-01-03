import os
from src.library import register_book, register_book_copy, get_book_id
import csv

def seed_library(path):
    full_path = os.path.join(os.path.dirname(__file__), f'../{path}')

    with open(full_path) as csvfile:
        reader =  csv.reader(csvfile)
        next(reader)
        for record in reader:
            authors = record[1]
            register_book(record[0], record[3], record[4], record[2], record[6], authors)
            book_id = get_book_id(record[0], record[3], record[4], record[2], record[6],)
            for copy in range(int(record[5])):
                register_book_copy(book_id, record[7])