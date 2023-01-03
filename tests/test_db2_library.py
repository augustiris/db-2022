import datetime
import unittest
from src.library import *
from tests.db2_csv_data_parser import seed_library

TEST_DATA_PATH = "data/Library_DB2.csv"
LOCATIONS_PATH = "data/insert_locations.sql"

class TestDB2Library(unittest.TestCase):

    def setUp(self):
        set_up(LOCATIONS_PATH)
        seed_library(TEST_DATA_PATH)

    def tearDown(self):
        pass

    """Test all .csv books loaded successfully into database"""
    def test_19_books(self):
        # setup
        expected = 19
        query = """
        SELECT COUNT(book_id)
        FROM library.books
        """
        # invoke
        actual = exec_get_all(query)[0][0]
        # analyze
        self.assertEqual(expected, actual)

    def test_search_for_available_book_copies_forty_two(self):
        expected = 42
        book_id = get_book_id("A Hitchhikers Guide to the Galaxy", "Fiction", "Science Fiction",
        "Don't panic", "8-18-1978")
        # invoke
        actual = len(search_for_available_book_copies(book_id))
        # analyze
        self.assertEqual(expected, actual)

    def test_search_for_available_book_copies_one(self):
        expected = 1
        book_id = get_book_id("A Brief History of Time", "Non-Fiction", "Science",
        "Any physical theory is always provisional",  "4/20/1961")
        # invoke
        actual = len(search_for_available_book_copies(book_id))
        # analyze
        self.assertEqual(expected, actual)

    def test_search_for_available_book_copies_none(self):
        register_user("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        user_id = get_user_id("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        book_id = get_book_id("A Brief History of Time", "Non-Fiction", "Science",
        "Any physical theory is always provisional",  "4/20/1961")
        copy_id = get_one_book_copy(book_id)
        checkout_book(user_id, copy_id, '2021-03-02')
        expected = 0
        # invoke
        actual = len(search_for_available_book_copies(book_id))
        # analyze
        self.assertEqual(expected, actual)

    def test_reserve_book_valid(self):
        # setup
        register_user("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        register_user('Jackie', None, 'Gleason', 'johngleason9870@gmail.com', '718-482-0234')
        user_id= get_user_id("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        book_id = get_book_id("A Brief History of Time", "Non-Fiction", "Science",
        "Any physical theory is always provisional",  "4/20/1961")
        copy_id = get_one_book_copy(book_id)
        checkout_book(user_id, copy_id, '2021-03-02')
        reserve_book(user_id, book_id)
        expected = ['A Brief History of Time']
        # invoke
        actual = get_all_reserved()
        # analyze
        self.assertEqual(expected, actual)

    def test_reserve_book_invalid(self):
        # setup
        register_user("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        register_user('Jackie', None, 'Gleason', 'johngleason9870@gmail.com', '718-482-0234')
        user_id= get_user_id("Mary", "Jane", "Smith", "jane754@gmail.com", "685-734-7654")
        book_id = get_book_id("A Hitchhikers Guide to the Galaxy", "Fiction", "Science Fiction",
        "Don't panic", "8-18-1978")
        copy_id = get_one_book_copy(book_id)
        checkout_book(user_id, copy_id, '2021-03-02')
        expected = "Unable to reserve book. 41 copies available for checkout."
        # invoke
        actual = reserve_book(user_id, book_id)
        # analyze
        self.assertEqual(expected, actual)

    def test_register_user_marlowe_and_bacon(self):
        # setup
        register_user("Christopher", None, "Marlowe", "marlow994@gmail.com", "215-734-7654")
        register_user("Francis", None, "Bacon", "bacon000@gmail.com", "602-214-0054")
        expected = [("Christopher", None, "Marlowe"), ("Francis", None, "Bacon")]
        # invoke
        actual = get_all_users()
        # analyze
        self.assertEqual(expected, actual)

    def test_returned_after_three_days(self):
        # setup
        borrowed_date = "2021-03-02"
        returned_date = "2021-03-05"
        register_user('Art', None, 'Garfunkel', 'art0123@gmail.com',  '347-423-5567')
        user_id = get_user_id('Art', None, 'Garfunkel', 'art0123@gmail.com',  '347-423-5567')
        book_id = get_book_id("A Hitchhikers Guide to the Galaxy", "Fiction", "Science Fiction",
        "Don't panic", "8-18-1978")
        book_copy_id = get_one_book_copy(book_id)
        checkout_book(user_id, book_copy_id, borrowed_date)
        checked_out_id = get_checked_out_id(user_id, book_copy_id, borrowed_date)
        return_book(returned_date, checked_out_id, book_copy_id)
        expected = 3
        # invoke
        actual = get_days_borrowed_after_returned(checked_out_id)
        # analyze
        self.assertEqual(expected, actual)

    def test_delete_user(self):
        # setup
        register_user("Christopher", None, "Marlowe", "marlow994@gmail.com", "215-734-7654")
        register_user("Francis", None, "Bacon", "bacon000@gmail.com", "602-214-0054")
        register_user('Mary', None, 'Shelley', 'mary453shell@gmail.com', '020-829-1023')
        register_user('Art', None, 'Garfunkel', 'art0123@gmail.com',  '347-423-5567')
        user_id = get_user_id('Mary', None, 'Shelley', 'mary453shell@gmail.com', '020-829-1023')
        delete_user(user_id)
        expected = [("Christopher", None, "Marlowe"), ("Francis", None, "Bacon"), 
        ('Art', None, 'Garfunkel')]
        # invoke
        actual = get_all_users()
        # analyze
        self.assertEqual(expected, actual)

    def test_get_checkout_log(self):
        # setup
        date1 = "2019-03-02"
        date2 = "2020-05-05"
        
        register_user("Christopher", None, "Marlowe", "marlow994@gmail.com", "215-734-7654")
        register_user("Francis", None, "Bacon", "bacon000@gmail.com", "602-214-0054")
        register_user('Mary', None, 'Shelley', 'mary453shell@gmail.com', '020-829-1023')
        user_id1 = get_user_id("Christopher", None, "Marlowe", "marlow994@gmail.com", "215-734-7654")
        user_id2 = get_user_id("Francis", None, "Bacon", "bacon000@gmail.com", "602-214-0054")
        user_id3 = get_user_id('Mary', None, 'Shelley', 'mary453shell@gmail.com', '020-829-1023')
        
        book_id1 = get_book_id("A Hitchhikers Guide to the Galaxy", "Fiction", "Science Fiction",
        "Don't panic", "8-18-1978")
        book_id2 = get_book_id("A Brief History of Time", "Non-Fiction", "Science",
        "Any physical theory is always provisional",  "4/20/1961")
        
        cp1 = get_one_book_copy(book_id1)
        checkout_book(user_id1, cp1, date1)
        cp2 = get_one_book_copy(book_id1)
        checkout_book(user_id2, cp2, date1)
        cp3 = get_one_book_copy(book_id2)
        checkout_book(user_id2, cp3, date1)
        cp4 = get_one_book_copy(book_id1)
        checkout_book(user_id3, cp4, date1)

        checked_out_id1 = get_checked_out_id(user_id1, cp1, date1)
        checked_out_id2 = get_checked_out_id(user_id2, cp3, date1)

        return_book(date2, checked_out_id1, cp1)
        return_book(date2, checked_out_id2, cp3)
        checkout_book(user_id3, cp1, date2)

        expected = [('A Hitchhikers Guide to the Galaxy', 'Douglas Adams', 'Fiction', 'Christopher Marlowe', datetime.date(2019, 3, 2), datetime.date(2020, 5, 5)),
        ('A Hitchhikers Guide to the Galaxy', 'Douglas Adams', 'Fiction', 'Francis Bacon', datetime.date(2019, 3, 2), None),
        ('A Hitchhikers Guide to the Galaxy', 'Douglas Adams', 'Fiction', 'Mary Shelley', datetime.date(2019, 3, 2), None),
        ('A Hitchhikers Guide to the Galaxy', 'Douglas Adams', 'Fiction', 'Mary Shelley', datetime.date(2020, 5, 5), None),
        ('A Brief History of Time', 'Stephen Hawking', 'Non-Fiction', 'Francis Bacon', datetime.date(2019, 3, 2), datetime.date(2020, 5, 5))]

        # invoke
        actual = get_checkout_log()

        # analyze
        self.assertEqual(expected, actual)

    if __name__ == '__main__':
        unittest.main()