import datetime
from traceback import print_tb
import unittest
from src.library import *

TEST_DATA_PATH = 'data/db3_test_data.sql'
week_one_overdue_fee = 0.25
overdue_fee = 2.00
ONE_WEEK = 7

class TestDB3Library(unittest.TestCase):

    def setUp(self):
        set_up(TEST_DATA_PATH)
        manually_sync_all_sequences()

    def tearDown(self):
        pass

    """
    GENERAL TESTS:
    """
    def test_zero_fees_due(self):
        # setup
        user_id = 1
        copy_id = 1

        checkout_book(user_id, copy_id, "2020-01-01")
        checkout_id = get_checked_out_id(user_id, copy_id, "2020-01-01")
        return_book("2020-01-05" , checkout_id, copy_id)
        expected = 0.0

        # invoke
        actual = get_fees_due(checkout_id)

        # analyze
        self.assertEqual(expected, actual)

    def test_one_hundred_twenty_five_cents_due(self):
        # setup
        user_id = 1
        copy_id = 1

        checkout_book(user_id, copy_id, "2020-01-01")
        checkout_id = get_checked_out_id(user_id, copy_id, "2020-01-01")
        return_book("2020-01-20" , checkout_id, copy_id)
        expected = 1.25

        # invoke
        actual = get_fees_due(checkout_id)

        # analyze
        self.assertEqual(expected, actual)

    """
    TEST CASES: A new book - the long awaited Game of Thrones installment,
        “The Winds of Winter”, by George R.R. Martin - is added to
        inventory with each library only having 1 copy. The follow checkouts
        occur @ Fairport.
    """
    # Mary checks it out on Jan. 2nd and returns in in 8 days.
    def test_mary_checkout(self):
        # setup
        register_book("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978", "George R.R. Martin")

        pittsford_id = 1
        henrietta_id = 2
        fairport_id = 3
        penfield_id = 4
        book_id = get_book_id("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978")
        register_book_copy(book_id, pittsford_id)
        register_book_copy(book_id, henrietta_id)
        register_book_copy(book_id, fairport_id)
        register_book_copy(book_id, penfield_id)
        mary_id = get_user_id('Mary', None, 'Shelley', 'mary453shell@gmail.com', '020-829-1023')
        copy_id = get_one_book_copy_at_location(book_id, fairport_id)

        checkout_book(mary_id, copy_id, "1951-01-02")
        checkout_id = get_checked_out_id(mary_id, copy_id, "1951-01-02")
        return_book("1951-01-10" , checkout_id, copy_id)
        expected = 8

        # invoke
        actual = get_days_borrowed_after_returned(checkout_id)

        # analyze
        self.assertEqual(expected, actual)

    # Ada checks it out on Jan 13th and returns it in 18 days.
    def test_ada_checkout(self):
        # setup
        register_book("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978", "George R.R. Martin")

        pittsford_id = 1
        henrietta_id = 2
        fairport_id = 3
        penfield_id = 4
        book_id = get_book_id("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978")
        register_book_copy(book_id, pittsford_id)
        register_book_copy(book_id, henrietta_id)
        register_book_copy(book_id, fairport_id)
        register_book_copy(book_id, penfield_id)
        mary_id = 2
        copy_id = get_one_book_copy_at_location(book_id, fairport_id)

        checkout_book(mary_id, copy_id, "1951-01-02")
        checkout_id = get_checked_out_id(mary_id, copy_id, "1951-01-02")
        return_book("1951-01-10" , checkout_id, copy_id)

        ada_id = 1
        checkout_book(ada_id, copy_id, "1951-01-13")
        checkout_id = get_checked_out_id(ada_id, copy_id, "1951-01-13")
        return_book("1951-01-31" , checkout_id, copy_id)

        expected = 18

        # invoke
        actual = get_days_borrowed_after_returned(checkout_id)

        # analyze
        self.assertEqual(expected, actual)

    # Ada tries to check out another book 15 days after checking out “The Winds of Winter”,
    # but her request is rejected due to the late status of her currently checked out book.
    def test_locked_user_ada_checkout(self):
        # setup
        date_one = "2022-01-01"
        date_two = "2022-01-31"

        register_book("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978", "George R.R. Martin")

        ada_id = 1
        fairport_id = 3
        book_id = get_book_id("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978")
        register_book_copy(book_id, fairport_id)
        register_book_copy(book_id, fairport_id)

        cp1_id = get_one_book_copy_at_location(book_id, fairport_id)
        checkout_book(ada_id, cp1_id, date_one)
        checkout_id = get_checked_out_id(ada_id, cp1_id, date_one)
        return_book(date_two, checkout_id, cp1_id)
        cp2_id = get_one_book_copy_at_location(book_id, fairport_id)
        
        late_fees = (ONE_WEEK * week_one_overdue_fee) + (((30 - ONE_WEEK*2) - ONE_WEEK) * overdue_fee)
        expected = "Account locked. $" + str(late_fees) + " due."

        # invoke
        actual = checkout_book(ada_id, cp2_id, date_two)

        # analyze
        self.assertEqual(expected, actual)

    # Jackie checks it out on March 1st and returns it in 30 days.
    def test_jackie_checkout(self):
        # setup

        register_book("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978", "George R.R. Martin")

        pittsford_id = 1
        henrietta_id = 2
        fairport_id = 3
        penfield_id = 4
        book_id = get_book_id("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978")
        register_book_copy(book_id, pittsford_id)
        register_book_copy(book_id, henrietta_id)
        register_book_copy(book_id, fairport_id)
        register_book_copy(book_id, penfield_id)
        jackie_id = 3
        copy_id = get_one_book_copy_at_location(book_id, fairport_id)

        checkout_book(jackie_id, copy_id, "1951-03-01")
        checkout_id = get_checked_out_id(jackie_id, copy_id, "1951-03-01")
        return_book("1951-03-31" , checkout_id, copy_id)

        expected = 30

        # invoke
        actual = get_days_borrowed_after_returned(checkout_id)

        # analyze
        self.assertEqual(expected, actual)

    # A good samaritan donates 3 additional copies of the ‘The Winds of Winter’ to Fairport.
    def test_winds_addition(self):
        # setup

        pittsford_id = 1
        henrietta_id = 2
        fairport_id = 3
        penfield_id = 4
        register_book("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978", "George R.R. Martin")
        book_id = get_book_id("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978")
        register_book_copy(book_id, pittsford_id)
        register_book_copy(book_id, henrietta_id)
        register_book_copy(book_id, fairport_id)
        register_book_copy(book_id, penfield_id)
        # The samaritan's donations
        register_book_copy(book_id, fairport_id)
        register_book_copy(book_id, fairport_id)
        register_book_copy(book_id, fairport_id)

        expected = 4

        # invoke
        actual = get_total_num_book_copies_at_location(book_id, fairport_id)

        # analyze
        self.assertEqual(expected, actual)

    # Another (attempted) good samaritan donates 2 copies of “The Wines of Winter”
    # by WineExpress to Pittsford and Henrietta.
    def test_wines_addition(self):
        # setup

        pittsford_id = 1
        henrietta_id = 2
        register_book("The Wines of Winter", "Fantasy", "Drama",
        "The long awaited Wines Series installment", "8/19/1978", "Wine Express")
        book_id = get_book_id("The Wines of Winter", "Fantasy", "Drama",
        "The long awaited Wines Series installment", "8/19/1978")
        # The samaritan's donations
        register_book_copy(book_id, pittsford_id)
        register_book_copy(book_id, henrietta_id)

        expected = 2

        # invoke
        actual = (get_total_num_book_copies_at_location(book_id, pittsford_id) +
            get_total_num_book_copies_at_location(book_id, henrietta_id)
        )

        # analyze
        self.assertEqual(expected, actual)

    # The Fairport Librarian runs a report listing overdue books per user.
    def test_overdue_list(self):
        # setup

        register_book("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978", "George R.R. Martin")

        pittsford_id = 1
        henrietta_id = 2
        fairport_id = 3
        penfield_id = 4

        book_id = get_book_id("The Winds of Winter", "Fantasy", "Drama",
        "The long awaited Game of Thrones installment", "8/18/1978")
        register_book_copy(book_id, pittsford_id)
        register_book_copy(book_id, henrietta_id)
        register_book_copy(book_id, fairport_id)
        register_book_copy(book_id, penfield_id)

        dateJ1 = '2022-01-1'
        dateJ2 = '2022-01-15'
        dateF1 = '2022-02-1'
        dateF2 = '2022-02-18'
        dateM1 = '2022-03-1'
        dateM2 = '2022-03-22'
        dateL1 = '2022-05-1'
        dateL2 = '2022-06-04'

        ada_id = 1
        mary_id = 2
        jackie_id = 3
        art_id = 4
        
        copy_id = get_one_book_copy_at_location(book_id, fairport_id)
        checkout_book(ada_id, copy_id, dateF1) #overdue
        checkout_1_id = get_checked_out_id(ada_id, copy_id, dateF1)
        return_book(dateF2, checkout_1_id, copy_id)

        checkout_book(mary_id, copy_id, dateM1) # overdue
        checkout_2_id = get_checked_out_id(mary_id, copy_id, dateM1)
        return_book(dateM2, checkout_2_id, copy_id)
        
        checkout_book(jackie_id, copy_id, dateL1) # overdue
        checkout_3_id = get_checked_out_id(jackie_id, copy_id, dateL1)
        return_book(dateL2, checkout_3_id, copy_id)

        checkout_book(art_id, copy_id, dateJ1)
        checkout_4_id =get_checked_out_id (art_id, copy_id, dateJ1)
        return_book(dateJ2, checkout_4_id, copy_id)

        expected = [('The Winds of Winter', 'Ada Lovelace', datetime.date(2022, 2, 1), 0.75),
        ('The Winds of Winter', 'Mary Shelley', datetime.date(2022, 3, 1), 1.75),
        ('The Winds of Winter', 'Jackie Gleason', datetime.date(2022, 5, 1), 27.75)]

        # invoke
        actual = get_overdue_list(fairport_id)

        # analyze
        self.assertEqual(expected, actual)

    # The county librarian runs a report listing all books in all books in all
    # libraries, organized by library location and book title with the count of
    # books at each location
    def test_all_libraries_report(self):
        # setup
        expected = [('A Hitchhikers Guide to the Galaxy', 'Adams', 2, 'Fairport Public Library'),
        ('A Hitchhikers Guide to the Galaxy', 'Adams', 2, 'Henrietta Public Library'),
        ('A Hitchhikers Guide to the Galaxy', 'Adams', 4, 'Penfield Public Library'),
        ('A Hitchhikers Guide to the Galaxy', 'Adams', 42, 'Pittsford Community Library'),
        ('The Invisible Man', 'Ellison', 7, 'Penfield Public Library'),
        ('The Invisible Man', 'Ellison', 13, 'Pittsford Community Library'), 
        ('The Invisible Man', 'Wells', 10, 'Fairport Public Library'),
        ('The Invisible Man', 'Wells', 3, 'Henrietta Public Library'), 
        ('The Invisible Man', 'Wells', 5, 'Pittsford Community Library')]

        # invoke
        actual = get_library_report()

        # analyze
        self.assertEqual(expected, actual)

    if __name__ == '__main__':
        unittest.main()