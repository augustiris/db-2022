import datetime
from decimal import Decimal
import unittest
from src.library import *

TEST_DATA_PATH = 'data/db4_test_data.sql'
week_one_overdue_fee = 0.25
overdue_fee = 2.00
ONE_WEEK = 7

class TestDB4Library(unittest.TestCase):

    def setUp(self):
        set_up(TEST_DATA_PATH)

    def tearDown(self):
        pass

    def test_checked_out_two_weeks_fees(self):
        # setup
        expected = 0.0

        date_one = '2022-08-1'
        date_two = '2022-08-15'
        ada_id = 1
        book_id = 1
        book_copy_id = get_one_book_copy(book_id)

        checkout_book(ada_id, book_copy_id, date_one)
        checkout_id = get_checked_out_id(ada_id, book_copy_id, date_one)
        return_book(date_two, checkout_id, book_copy_id)

        # invoke
        update_all_fees_due(date_two)
        actual = get_fees_due(checkout_id)

        # analyze
        self.assertEqual(expected, actual)

    def test_three_days_overdue(self):
        # setup
        expected = 3 * week_one_overdue_fee

        date_one = '2022-08-1'
        date_two = '2022-08-18'
        ada_id = 1
        book_id = 1
        book_copy_id = get_one_book_copy(book_id)

        checkout_book(ada_id, book_copy_id, date_one)
        checkout_id = get_checked_out_id(ada_id, book_copy_id, date_one)
        return_book(date_two, checkout_id, book_copy_id)

        # invoke
        update_all_fees_due(date_two)
        actual = get_fees_due(checkout_id)

        # analyze
        self.assertEqual(expected, actual)

    def test_seven_days_overdue(self):
        # setup
        expected = ONE_WEEK * week_one_overdue_fee

        date_one = '2022-08-1'
        date_two = '2022-08-22'
        ada_id = 1
        book_id = 1
        book_copy_id = get_one_book_copy(book_id)

        checkout_book(ada_id, book_copy_id, date_one)
        checkout_id = get_checked_out_id(ada_id, book_copy_id, date_one)
        return_book(date_two, checkout_id, book_copy_id)

        # invoke
        update_all_fees_due(date_two)
        actual = get_fees_due(checkout_id)

        # analyze
        self.assertEqual(expected, actual)

    def test_eight_days_overdue(self):
        # setup
        expected = (ONE_WEEK * week_one_overdue_fee) + (overdue_fee)

        date_one = '2022-08-1'
        date_two = '2022-08-23'
        ada_id = 1
        book_id = 1
        book_copy_id = get_one_book_copy(book_id)

        checkout_book(ada_id, book_copy_id, date_one)
        checkout_id = get_checked_out_id(ada_id, book_copy_id, date_one)
        return_book(date_two, checkout_id, book_copy_id)

        # invoke
        update_all_fees_due(date_two)
        actual = get_fees_due(checkout_id)

        # analyze
        self.assertEqual(expected, actual)

        # analyze
        self.assertEqual(expected, actual)

    def test_twenty_days_overdue(self):
        # setup
        expected = (ONE_WEEK * week_one_overdue_fee) + ((20 - ONE_WEEK) * overdue_fee)

        date_one = '2022-08-1'
        date_two = '2022-09-04'
        ada_id = 1
        book_id = 1
        book_copy_id = get_one_book_copy(book_id)

        checkout_book(ada_id, book_copy_id, date_one)
        checkout_id = get_checked_out_id(ada_id, book_copy_id, date_one)
        return_book(date_two, checkout_id, book_copy_id)

        # invoke
        update_all_fees_due(date_two)
        actual = get_fees_due(checkout_id)

        # analyze
        self.assertEqual(expected, actual)

        # analyze
        self.assertEqual(expected, actual)

    def test_book_checkout_table(self):
        # setup
        expected = [(['A Hitchhikers Guide to the Galaxy by Douglas Adams'], ['Mary Shelley'], datetime.date(2022, 1, 1), datetime.date(2022, 1, 15), 0.0), # returned on time
        (['Good Omens by Neil Gaiman', 'Good Omens by Terry Pratchett'], ['Mary Shelley'], datetime.date(2022, 1, 1), None, 0.0), # still checked out (the book has two authors)
        (['A Hitchhikers Guide to the Galaxy by Douglas Adams'], ['Ada Lovelace'], datetime.date(2022, 2, 1), datetime.date(2022, 2, 18), 0.75), # returned 3 days late
        (['The Catcher in the Rye by Jerome Salinger'], ['Ada Lovelace'], datetime.date(2022, 2, 1), datetime.date(2022, 2, 18), 0.75), # returned 3 days late
        (['To Kill a Mockingbird by Harper Lee'], ['Ada Lovelace'], datetime.date(2022, 2, 1), datetime.date(2022, 2, 18), 0.75), # returned 3 days late
        (['The Invisible Man by Ralph Ellison'], ['Jackie Gleason'], datetime.date(2022, 3, 1), datetime.date(2022, 3, 22), 1.75), # returned 7 days late
        (['To Kill a Mockingbird by Harper Lee'], ['Jackie Gleason'], datetime.date(2022, 3, 1), datetime.date(2022, 3, 22), 1.75), # returned 7 days late
        (['Go Set a Watchman by Harper Lee'], ['Art Garfunkel'], datetime.date(2022, 5, 1), None, 0.0), # still checked out
        (['To Kill a Mockingbird by Harper Lee'], ['Art Garfunkel'], datetime.date(2022, 5, 1), datetime.date(2022, 6, 4), 27.75)] # returned 20 days late
        
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

        hitchhikers_book_id = 1
        invisible_book_id = 2
        mockingbird_book_id = 3
        watchman_book_id = 4
        rye_book_id = 5
        good_book_id = 6

        h_book_copy_1 = get_one_book_copy_at_location(hitchhikers_book_id, 1)
        h_book_copy_2 = get_one_book_copy_at_location(hitchhikers_book_id, 2)
        i_book_copy_1 = get_one_book_copy(invisible_book_id)
        m_book_copy_1 = get_one_book_copy_at_location(mockingbird_book_id, 1)
        m_book_copy_2 = get_one_book_copy_at_location(mockingbird_book_id, 2)
        m_book_copy_3 = get_one_book_copy_at_location(mockingbird_book_id, 3)
        w_book_copy_1 = get_one_book_copy(watchman_book_id)
        r_book_copy_1 = get_one_book_copy(rye_book_id)
        g_book_copy_1 = get_one_book_copy(good_book_id)

        # total of 9 books in history
        checkout_book(ada_id, r_book_copy_1, dateF1) # ada
        checkout_book(ada_id, h_book_copy_1, dateF1)
        checkout_book(ada_id, m_book_copy_1, dateF1)
        checkout_book(mary_id, h_book_copy_2, dateJ1) # mary
        checkout_book(mary_id, g_book_copy_1, dateJ1)
        checkout_book(jackie_id, i_book_copy_1, dateM1) # jackie
        checkout_book(jackie_id, m_book_copy_3, dateM1)
        checkout_book(art_id, m_book_copy_2, dateL1) # art
        checkout_book(art_id, w_book_copy_1, dateL1)

        c1 = get_checked_out_id(ada_id, r_book_copy_1, dateF1)
        c2 = get_checked_out_id(ada_id, h_book_copy_1, dateF1)
        c3 = get_checked_out_id(ada_id, m_book_copy_1, dateF1)
        c4 = get_checked_out_id(mary_id, h_book_copy_2, dateJ1)
        c5 = get_checked_out_id(jackie_id, i_book_copy_1, dateM1)
        c6 = get_checked_out_id(jackie_id, m_book_copy_3, dateM1)
        c7 = get_checked_out_id(art_id, m_book_copy_2, dateL1)

        # 7 books returned
        return_book(dateF2, c1, r_book_copy_1)
        return_book(dateF2, c2, h_book_copy_1)
        return_book(dateF2, c3, m_book_copy_1)
        return_book(dateJ2, c4, h_book_copy_2)
        return_book(dateM2, c5, i_book_copy_1)
        return_book(dateM2, c6, i_book_copy_1)
        return_book(dateL2, c7, m_book_copy_2)

        # invoke
        actual = get_book_checkout_table()

        # analyze
        self.assertEqual(expected, actual)

    def test_get_full_user_info(self):
        # setup
        expected = [(['Mary Shelley'], ['A Hitchhikers Guide to the Galaxy by Douglas Adams'], datetime.date(2022, 1, 1), datetime.date(2022, 1, 15), 0.0),
        (['Mary Shelley'], ['Good Omens by Terry Pratchett', 'Good Omens by Neil Gaiman'], datetime.date(2022, 1, 1), datetime.date(2022, 1, 15), 0.0),
        (['Mary Shelley'], ['The Invisible Man by Ralph Ellison'], datetime.date(2022, 2, 1), None, 0.0),
        (['Mary Shelley'], ['To Kill a Mockingbird by Harper Lee'], datetime.date(2022, 2, 1), datetime.date(2022, 2, 18), 0.75)]

        dateJ1 = '2022-01-1'
        dateJ2 = '2022-01-15'
        dateF1 = '2022-02-1'
        dateF2 = '2022-02-18'

        mary_id = 2

        hitchhikers_book_id = 1
        invisible_book_id = 2
        mockingbird_book_id = 3
        good_book_id = 6

        h_book_copy_1 = get_one_book_copy_at_location(hitchhikers_book_id, 1)
        g_book_copy_1 = get_one_book_copy(good_book_id)
        i_book_copy_1 = get_one_book_copy(invisible_book_id)
        m_book_copy_1 = get_one_book_copy_at_location(mockingbird_book_id, 1)

        checkout_book(mary_id, h_book_copy_1, dateJ1)
        checkout_book(mary_id, g_book_copy_1, dateJ1)

        c1 = get_checked_out_id(mary_id, h_book_copy_1, dateJ1)
        c2 = get_checked_out_id(mary_id, g_book_copy_1, dateJ1)

        return_book(dateJ2, c1, h_book_copy_1) # return on time
        return_book(dateJ2, c2, g_book_copy_1) # return on time

        checkout_book(mary_id, i_book_copy_1, dateF1)
        checkout_book(mary_id, m_book_copy_1, dateF1)

        c3 = get_checked_out_id(mary_id, m_book_copy_1, dateF1)
        return_book(dateF2, c3, i_book_copy_1) # return 3 days late

        # invoke
        actual = get_full_user_info(mary_id)

        # analyze
        self.assertEqual(expected, actual)

    def test_book_checked_out_books_report(self):
        # setup
        expected = ([('A Hitchhikers Guide to the Galaxy', ['Mary Shelley'], datetime.date(2022, 1, 1), datetime.date(2022, 1, 15), 14),
        ('Good Omens', ['Mary Shelley'], datetime.date(2022, 1, 1), None, None),
        ('A Hitchhikers Guide to the Galaxy', ['Ada Lovelace'], datetime.date(2022, 2, 1), datetime.date(2022, 2, 18), 17),
        ('The Catcher in the Rye', ['Ada Lovelace'], datetime.date(2022, 2, 1), datetime.date(2022, 2, 18), 17),
        ('To Kill a Mockingbird', ['Ada Lovelace'], datetime.date(2022, 2, 1), datetime.date(2022, 2, 18), 17),
        ('The Invisible Man', ['Jackie Gleason'], datetime.date(2022, 3, 1), datetime.date(2022, 3, 22), 21),
        ('To Kill a Mockingbird', ['Jackie Gleason'], datetime.date(2022, 3, 1), datetime.date(2022, 3, 22), 21),
        ('Go Set a Watchman', ['Art Garfunkel'], datetime.date(2022, 5, 1), None, None),
        ('To Kill a Mockingbird', ['Art Garfunkel'], datetime.date(2022, 5, 1), datetime.date(2022, 6, 4), 34)],
        Decimal('20.14')) # books are checked out for an avg of 20 days

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

        hitchhikers_book_id = 1
        invisible_book_id = 2
        mockingbird_book_id = 3
        watchman_book_id = 4
        rye_book_id = 5
        good_book_id = 6

        h_book_copy_1 = get_one_book_copy_at_location(hitchhikers_book_id, 1)
        h_book_copy_2 = get_one_book_copy_at_location(hitchhikers_book_id, 2)
        i_book_copy_1 = get_one_book_copy(invisible_book_id)
        m_book_copy_1 = get_one_book_copy_at_location(mockingbird_book_id, 1)
        m_book_copy_2 = get_one_book_copy_at_location(mockingbird_book_id, 2)
        m_book_copy_3 = get_one_book_copy_at_location(mockingbird_book_id, 3)
        w_book_copy_1 = get_one_book_copy(watchman_book_id)
        r_book_copy_1 = get_one_book_copy(rye_book_id)
        g_book_copy_1 = get_one_book_copy(good_book_id)

        # total of 9 books in history
        checkout_book(ada_id, r_book_copy_1, dateF1) # ada
        checkout_book(ada_id, h_book_copy_1, dateF1)
        checkout_book(ada_id, m_book_copy_1, dateF1)
        checkout_book(mary_id, h_book_copy_2, dateJ1) # mary
        checkout_book(mary_id, g_book_copy_1, dateJ1)
        checkout_book(jackie_id, i_book_copy_1, dateM1) # jackie
        checkout_book(jackie_id, m_book_copy_3, dateM1)
        checkout_book(art_id, m_book_copy_2, dateL1) # art
        checkout_book(art_id, w_book_copy_1, dateL1)

        c1 = get_checked_out_id(ada_id, r_book_copy_1, dateF1)
        c2 = get_checked_out_id(ada_id, h_book_copy_1, dateF1)
        c3 = get_checked_out_id(ada_id, m_book_copy_1, dateF1)
        c4 = get_checked_out_id(mary_id, h_book_copy_2, dateJ1)
        c5 = get_checked_out_id(jackie_id, i_book_copy_1, dateM1)
        c6 = get_checked_out_id(jackie_id, m_book_copy_3, dateM1)
        c7 = get_checked_out_id(art_id, m_book_copy_2, dateL1)

        # 7 books returned
        return_book(dateF2, c1, r_book_copy_1)
        return_book(dateF2, c2, h_book_copy_1)
        return_book(dateF2, c3, m_book_copy_1)
        return_book(dateJ2, c4, h_book_copy_2)
        return_book(dateM2, c5, i_book_copy_1)
        return_book(dateM2, c6, i_book_copy_1)
        return_book(dateL2, c7, m_book_copy_2)

        # invoke
        actual = get_checked_out_books_report()

        # analyze
        self.assertEqual(expected, actual)

    if __name__ == '__main__':
        unittest.main()