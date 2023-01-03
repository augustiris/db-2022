import unittest
from src.library import *
from src.swen344_db_utils import connect

TEST_DATA_PATH = 'data/db1_test_data.sql'

class TestDB1Library(unittest.TestCase):

    def setUp(self):
        set_up(TEST_DATA_PATH)

    def tearDown(self):
        pass

    def test_get_author_id(self):
        expected = 1
        actual = get_author_id('Henry', 'David', 'Thoreau')
        self.assertEqual(expected, actual)

    def test_get_book(self):
        expected = [('The Catcher in the Rye', 'Bob Evans,Jane Smith,Jerome Salinger')]
        book_id = 6
        actual = get_book(book_id)
        self.assertEqual(expected, actual)

    def test_get_book_one_author(self):
        expected = [('Henry', 'David', 'Thoreau')]
        actual = get_book_authors(1)
        self.assertEqual(expected, actual)

    def test_get_book_multiple_authors(self):
        expected = [('Jerome', 'David', 'Salinger'),
        ('Bob', 'Lloyd', 'Evans'),
        ('Jane', 'Mary', 'Smith')]
        actual = get_book_authors(6)
        self.assertEqual(expected, actual)

    def test_num_book_copies_ten(self):
        expected = 10
        actual = get_total_num_book_copies(4)
        self.assertEqual(expected, actual)

    def test_num_book_copies_zero(self):
        expected = 0
        actual = get_total_num_book_copies(4000)
        self.assertEqual(expected, actual)

    def test_get_all_authors(self):
        expected = [('Henry', 'David', 'Thoreau'),
        ('Charles', None, 'Darwin'),
        ('Benjamin', None, 'Franklin'),
        ('Harper', None, 'Lee'),
        ('Jerome', 'David', 'Salinger'),
        ('Bob', 'Lloyd', 'Evans'),
        ('Jane', 'Mary', 'Smith')]
        actual = get_all_authors()
        self.assertEqual(expected, actual)

    def test_get_all_books(self):
        expected = [('Go Set a Watchman', 'Harper Lee'), ('The Autobiography of Benjamin Franklin', 'Benjamin Franklin'),
        ('The Autobiography of Charles Darwin', 'Charles Darwin'), ('The Catcher in the Rye', 'Bob Evans,Jane Smith,Jerome Salinger'),
        ('To Kill a Mockingbird', 'Harper Lee'), ('Walden', 'Henry Thoreau')]
        actual = get_all_books()
        self.assertEqual(expected, actual)

    def test_get_all_users(self):
        expected = [('Ada', None, 'Lovelace'), ('Mary', None, 'Shelley'), 
        ('Jackie', None, 'Gleason'), ('Art', None, 'Garfunkel')]
        actual = get_all_users()
        self.assertEqual(expected, actual)

    def test_get_user_id(self):
        expected = 1
        actual = get_user_id('Ada', None, 'Lovelace', 'lovelace321@gmail.com', '020-321-1029')
        self.assertEqual(expected, actual)

    def test_art_checked_out_none(self):
        expected = []
        art_id = 4
        actual = get_checked_out(art_id)
        self.assertEqual(expected, actual)

    def test_gleason_checked_out(self):
        expected = ['Go Set a Watchman', 28, 'The Catcher in the Rye', 30, 'To Kill a Mockingbird', 23]
        gleason_id = 3
        actual = get_checked_out(gleason_id)
        self.assertEqual(expected, actual)

    def test_get_all_nonfiction_and_quantity(self):
        expected = (['Walden', 'The Autobiography of Charles Darwin', 'The Autobiography of Benjamin Franklin'], 3)
        actual = get_all_of_genre('non-fiction')
        self.assertEqual(expected, actual)

    def test_rebuild_authors_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        rebuild_tables()
        rebuild_tables()
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM library.authors')
        self.assertEqual([], cur.fetchall(), "no rows in library.authors")
        conn.close()

    if __name__ == '__main__':
        unittest.main()