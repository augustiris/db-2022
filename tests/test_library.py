import unittest
from src.library import *

TEST_DATA_PATH = 'data/insert_locations.sql'

class TestLibrary(unittest.TestCase):

    def setUp(self):
        set_up(TEST_DATA_PATH)

    def tearDown(self):
        pass

    def test_is_checked_out_true(self):
        # setup
        register_user("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        user_id = get_user_id("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        register_book('Walden', 'non-fiction', 'memoir', 'testSummary', '1854-08-09',
        'Henry David Thoreau')
        book_id = get_book_id('Walden', 'non-fiction', 'memoir', 'testSummary', '1854-08-09')
        register_book_copy(book_id, 1)
        book_copy_id = get_one_book_copy(book_id)
        checkout_book(user_id, book_copy_id, '1854-08-09')
        expected = True
        # invoke
        actual = is_checked_out(book_copy_id)
        # analyze
        self.assertEqual(expected, actual)

    def test_is_checked_out_false(self):
        # setup
        register_book('Walden', 'non-fiction', 'memoir', 'testSummary', '1854-08-09',
        'Henry David Thoreau')
        book_id = get_book_id('Walden', 'non-fiction', 'memoir', 'testSummary', '1854-08-09')
        register_book_copy(book_id, 1)
        book_copy_id = get_one_book_copy(book_id)
        expected = False
        # invoke
        actual = is_checked_out(book_copy_id)
        # analyze
        self.assertEqual(expected, actual)

    def test_register_book_one_author(self):
        # setup
        register_book('Walden', 'non-fiction', 'memoir', 'testSummary', '1854-08-09',
        'Henry David Thoreau')
        book_id = get_book_id('Walden', 'non-fiction', 'memoir', 'testSummary', '1854-08-09')
        expected = [('Walden', ('Henry Thoreau'))]
        # invoke
        actual = get_book(book_id)
        # analyze
        self.assertEqual(expected, actual)

    def test_register_book_multiple_authors(self):
        # setup
        register_book('The Catcher in the Rye', 'fiction', 'young adult', 'This is a test', '1951-07-16',
        'Bob Evans,Jane Smith,Jerome Salinger')
        book_id = get_book_id('The Catcher in the Rye', 'fiction', 'young adult', 'This is a test', '1951-07-16')
        expected = [('The Catcher in the Rye', 'Bob Evans,Jane Smith,Jerome Salinger')]
        # invoke
        actual = get_book(book_id)
        # analyze
        self.assertEqual(expected, actual)

    def test_register_one_book_copy(self):
        # setup
        register_author('Henry', 'David', 'Thoreau')
        register_book('Walden', 'non-fiction', 'memoir', 'This is a book', '1854-08-09', 'Henry David Thoreau')
        book_id = get_book_id('Walden', 'non-fiction', 'memoir', 'This is a book', '1854-08-09')
        register_book_copy(book_id, 1)
        expected = 1
        # invoke
        actual = get_total_num_book_copies(book_id)
        # analyze
        self.assertEqual(expected, actual)

    def test_register_ten_book_copies(self):
        register_author('Henry', 'David', 'Thoreau')
        register_book('Walden', 'non-fiction', 'memoir', 'This is a book', '1854-08-09', 'Henry David Thoreau')
        book_id = get_book_id('Walden', 'non-fiction', 'memoir', 'This is a book', '1854-08-09')
        for copy in range(10):
            register_book_copy(book_id, 1)
        expected = 10
        # invoke
        actual = get_total_num_book_copies(book_id)
        # analyze
        self.assertEqual(expected, actual)

    def test_checkout_book_pass(self):
        register_user("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        user_id = get_user_id("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        register_author('Henry', 'David', 'Thoreau')
        register_book('Walden', 'non-fiction', 'memoir', 'This is a book', '1854-08-09', 'Henry David Thoreau')
        book_id = get_book_id('Walden', 'non-fiction', 'memoir', 'This is a book', '1854-08-09')
        register_book_copy(book_id, 1)
        copy_id = get_one_book_copy(book_id)
        checkout_book(user_id, copy_id, '2021-03-02')
        expected = ['Walden', 1]
        # invoke
        actual = get_checked_out(user_id)
        # analyze
        self.assertEqual(expected, actual)

    def test_checkout_book_already_checked_out(self):
        register_user("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        register_user("Billy", "Bob", "Joe", "jo@gmail.com", "685-876-7734")
        user_id_one = get_user_id("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        user_id_two = get_user_id("Billy", "Bob", "Joe", "jo@gmail.com", "685-876-7734")
        register_author('Henry', 'David', 'Thoreau')
        register_book('Walden', 'non-fiction', 'memoir', 'This is a book', '1854-08-09', 'Henry David Thoreau')
        book_id = get_book_id('Walden', 'non-fiction', 'memoir', 'This is a book', '1854-08-09')
        register_book_copy(book_id, 1)
        copy_id = get_one_book_copy(book_id)
        checkout_book(user_id_one, copy_id, '2021-03-02')
        expected = "Copy already checked out by another user."
        # invoke
        actual = checkout_book(user_id_two, copy_id, '2021-03-02')
        # analyze
        self.assertEqual(expected, actual)