from src.swen344_db_utils import connect, exec_sql_file, exec_get_all, exec_commit

# One week is 7 days (used for calculating due dates and fees)
ONE_WEEK = 7

"""
SETUP
"""
# Drops all the tables and schema for library
def drop_tables_and_schema() -> None:
    conn = connect()
    cur = conn.cursor()
    drop_sql = """ 
    DROP SCHEMA IF EXISTS library CASCADE;
    DROP TABLE IF EXISTS library.locations CASCADE;
    DROP TABLE IF EXISTS library.reserved CASCADE;
    DROP TABLE IF EXISTS library.checked_out CASCADE;
    DROP TABLE IF EXISTS library.users CASCADE;
    DROP TABLE IF EXISTS library.book_copies CASCADE;
    DROP TABLE IF EXISTS library.books CASCADE;
    DROP TABLE IF EXISTS library.wrote CASCADE;
    DROP TABLE IF EXISTS library.authors CASCADE;
    """
    cur.execute(drop_sql)
    conn.close()

"""
Drops all the tables and schema for library then builds them
again.
"""
def rebuild_tables() -> None:
    drop_tables_and_schema()
    sql_create_path = 'src/library_build.sql'
    exec_sql_file(sql_create_path)

"""
Rebuilds the tables and schema and if the file path
is not null it excutes it
"""
def set_up(test_data_path) -> None:
    rebuild_tables()
    if test_data_path is not None:
        exec_sql_file(test_data_path)

"""
The primary keys get out of sync when there's a mix of hardcoding them
and using "Serial" to generate them automatically in tests. This
function makes sure that the next key auto generated is available.
"""
def manually_sync_all_sequences() -> None:
    query = """
        SELECT pg_catalog.setval(pg_get_serial_sequence('library.books', 'book_id'),
            (SELECT MAX(book_id) FROM library.books));
        SELECT pg_catalog.setval(pg_get_serial_sequence('library.locations', 'location_id'),
            (SELECT MAX(location_id) FROM library.locations));
        SELECT pg_catalog.setval(pg_get_serial_sequence('library.users', 'user_id'),
            (SELECT MAX(user_id) FROM library.users));
        SELECT pg_catalog.setval(pg_get_serial_sequence('library.authors', 'author_id'),
            (SELECT MAX(author_id) FROM library.authors));
        """
    return exec_commit(query,)

"""
CREATE
"""
"""
Inserts an author record into library.authors
"""
def register_author(first_name, middle_name, last_name) -> None:
    query = """
        INSERT INTO library.authors (first_name, middle_name, last_name)
        VALUES (%s, %s, %s)
        """
    exec_commit(query, (first_name, middle_name, last_name))

"""
Inserts a book record into library.books
For each comma separated author in authors (passed in the parameter) a
    record is created in library.authors and a record is created in
    library.wrote if no id is found for them.
"""
def register_book(title, genre, sub_genre, summary, publish_date, authors) -> None:
    query = """
    INSERT INTO library.books(title, genre, sub_genre, summary, publish_date)
    VALUES (%s, %s, %s, %s, %s)
    """
    exec_commit(query, (title, genre, sub_genre, summary, publish_date))
    book_id = get_book_id(title, genre, sub_genre, summary, publish_date)

    authors = authors.split(',')
    for author in authors:
        author = author.split(' ')
        first = author[0]
        middle = None if len(author) == 2 else author[1]
        last = author[1] if len(author) == 2 else author[2]
        if get_author_id(first, middle, last) == "Author not registered":
            register_author(first, middle, last)
        author_id = get_author_id(first, middle, last)
        query = """    
        INSERT INTO library.wrote (author_id, book_id)
        VALUES (%s, %s)
        """
        exec_commit(query, (author_id, book_id))

"""
Inserts a book copy record into library.book_copies
"""
def register_book_copy(book_id, location_id) -> None:
    query = """
        INSERT INTO library.book_copies (book_id, location_id)
        VALUES (%s, %s)
        """
    exec_commit(query, (book_id, location_id))

"""
Inserts a user record into library.users
"""
def register_user(first_name, middle_name, last_name, email, phone) -> None:
    query = """
        INSERT INTO library.users (first_name, middle_name, last_name, email, phone)
        VALUES (%s, %s, %s, %s, %s)
        """
    exec_commit(query, (first_name, middle_name, last_name, email, phone))

"""
Given a book_id it searches for available copies. If there are copies available
a message is returned saying that the book cannot be reserved. Else a reserve
record is created in library.reserved
"""
def reserve_book(user_id, book_id) -> None:
    result = search_for_available_book_copies(book_id)
    num_of_available_copies = len(result)

    if num_of_available_copies < 1:
        query = """
            INSERT INTO library.reserved (user_id, book_id)
            VALUES (%s, %s)
            """
        return exec_commit(query, (user_id, book_id))

    return "Unable to reserve book. " + str(num_of_available_copies) + " copies available for checkout."

"""
Checks to see if the user has any unpaid fees associated with their account.
If they do they cannot check out any books. If the book copy is not already 
checked out, a record is created in library.checked_out
"""
def checkout_book(user_id, book_copy_id, current_date) -> str:
    outstanding_fees = get_all_fees_due(get_all_checked_out_ids(user_id))
    if outstanding_fees > 0.0:
        message = "Account locked. $" + str(outstanding_fees) + " due."
        print(message)
        return message

    if not is_checked_out(book_copy_id):
        query = """
            INSERT INTO library.checked_out (user_id, book_copy_id, borrowed_date)
            VALUES (%s, %s, %s);
            UPDATE library.book_copies
            SET is_checked_out = true
            WHERE book_copies.book_copy_id=%s
            """
        message = "User #" + str(user_id) + " checked out Book Copy #" + str(book_copy_id)
        # print(message)
        exec_commit(query, (user_id, book_copy_id, current_date, book_copy_id))
        return message

    message = "Copy already checked out by another user."
    print(message)
    return message

"""
DELETE
"""
"""
Removes a user's account from library.users given a user_id
"""
def delete_user(user_id) -> None:
    try:
        query = """
            DELETE FROM library.users
            WHERE user_id=%s
            """
        result = exec_commit(query, (user_id,))
    except:
        return "User not found. Cannot delete."
    return result

"""
UPDATE
"""
"""
Given a check_out_id and the number of days borrowed,
calculates the fees due and updates the record
associated with the id.
"""
def update_fee(days_borrowed, checked_out_id) -> float:
    amount_due = 0.0
    week_one_penalty = 0.25
    penalty = 2.00
    days_overdue = days_borrowed - (ONE_WEEK * 2)

    # If the book is overdue for any amount of days
    if(days_overdue > 0):
        # If the book has been overdue for more than a week they must pay a penalty of $2.00
        if(days_overdue > ONE_WEEK):
            amount_due += (days_overdue - ONE_WEEK) * penalty
        # For the first week the penalty is only $0.25
        amount_due += ((ONE_WEEK) * week_one_penalty) if (days_overdue > ONE_WEEK) else (days_overdue * week_one_penalty)

    query = """
    UPDATE library.checked_out
    SET fees_due=%s
    WHERE checked_out.checked_out_id=%s;
    """
    exec_commit(query, (amount_due, checked_out_id))

    return amount_due

"""
Updates the checked_out record associated with the given id
with the date returned and updates the book copies with 
the given id to is_checked_out = false
"""
def return_book(return_date, checked_out_id, book_copy_id) -> None:
    query = """
        UPDATE library.checked_out
        SET returned_date=%s
        WHERE checked_out.checked_out_id=%s;
        UPDATE library.book_copies
        SET is_checked_out = false
        WHERE book_copies.book_copy_id=%s
        """
    exec_commit(query, (return_date, checked_out_id, book_copy_id))
    days_borrowed = get_days_borrowed_after_returned(checked_out_id)
    late_fees = update_fee(days_borrowed, checked_out_id)
    if (days_borrowed > 14):
        print("You returned your book " + str(days_borrowed - 14) + 
        " days late. You have a late fee of " +
        "${:.2f}".format(late_fees))

"""
For all users in the database gets their checkout history and
updates their fees due, given a current date.
"""
def update_all_fees_due(current_date) -> None:
    user_ids = get_all_users_ids()
    for id in user_ids:
        for checked_out_id in get_all_checked_out_ids(id):
            update_fee(get_days_borrowed(checked_out_id, current_date), checked_out_id)

"""
READ
"""
"""
Generates a report that lists each book that has been checked out,
the number of days for which it was checked out, prints the average
number of days it takes for a book to be returned. 
"""
def get_checked_out_books_report():
    query = """
    SELECT
        books.title,
        ARRAY_AGG (
            users.first_name || ' ' || users.last_name
        ) patrons,
        checked_out.borrowed_date,
        checked_out.returned_date,
        checked_out.days_borrowed

    FROM library.checked_out
    INNER JOIN library.book_copies USING (book_copy_id)
    INNER JOIN library.books USING (book_id)
    INNER JOIN library.users USING (user_id)
    GROUP BY
        books.title,
        checked_out.borrowed_date,
        checked_out.returned_date,
        checked_out.days_borrowed
    ORDER BY checked_out.borrowed_date ASC
    """
    book_report = exec_get_all(query, )
    
    query = """
    SELECT AVG(checked_out.days_borrowed)::numeric(10,2)
    FROM library.checked_out
    """
    avg_return_time = exec_get_all(query, )[0][0]
    print("Average return time = " + str(avg_return_time) + " days")

    return book_report, avg_return_time

"""
Presents a table style listing of each book and who has checked out the book.
Make the output user friendly by have all the book info (title/author)
in ONE column in the output
"""
def get_book_checkout_table():
    query = """
    SELECT
        ARRAY_AGG (
            books.title || ' by ' || authors.first_name || ' ' || authors.last_name
        ) book_and_authors_list,
        ARRAY_AGG (
            DISTINCT CONCAT(users.first_name || ' ' || users.last_name)
        ) patrons,
        checked_out.borrowed_date,
        checked_out.returned_date,
        checked_out.fees_due
    FROM library.checked_out
    INNER JOIN library.book_copies USING (book_copy_id)
    INNER JOIN library.books USING (book_id)
    INNER JOIN library.wrote USING (book_id)
    INNER JOIN library.authors USING (author_id)
    INNER JOIN library.users USING (user_id)
    GROUP BY
        books.title,
        checked_out.borrowed_date,
        checked_out.returned_date,
        checked_out.fees_due
    ORDER BY checked_out.borrowed_date ASC
    """

    result = exec_get_all(query, )
    return result

"""
User information for all activity. This includes the user name, books checked out,
due dates, return dates and late fees. Organize by library, user, books and date
"""
def get_full_user_info(user_id):
    query = """
    SELECT
        ARRAY_AGG (
            DISTINCT CONCAT(users.first_name || ' ' || users.last_name)
        ) patron,
        ARRAY_AGG (
            books.title || ' by ' || authors.first_name || ' ' || authors.last_name
        ) book_and_authors_list,
        checked_out.borrowed_date,
        checked_out.returned_date,
        checked_out.fees_due

    FROM library.checked_out
    INNER JOIN library.book_copies USING (book_copy_id)
    INNER JOIN library.books USING (book_id)
    INNER JOIN library.wrote USING (book_id)
    INNER JOIN library.authors USING (author_id)
    INNER JOIN library.users USING (user_id)
    WHERE library.users.user_id=%s
    GROUP BY
        books.title,
        checked_out.borrowed_date,
        checked_out.returned_date,
        checked_out.fees_due
    ORDER BY checked_out.borrowed_date ASC
    """

    result = exec_get_all(query, (user_id,))
    return result

"""
Returns a list of all library books including their title, authors, copy count,
and locations
"""
def get_library_report():
    query = """
    SELECT books.title,
        authors.last_name,
        COUNT(book_copy_id),
        locations.title

        FROM library.books
        INNER JOIN library.wrote USING (book_id)
        INNER JOIN library.authors USING (author_id)
        INNER JOIN library.book_copies USING (book_id)
        INNER JOIN library.locations USING (location_id)

        GROUP BY books.title,
            authors.first_name, authors.last_name,
            locations.title
        ORDER BY books.title, authors.last_name
    """
    result = exec_get_all(query, )
    return result

"""
Updates all fees due for all users and then returns a list of
overdue books given a location and date
"""
def get_overdue_list(location_id, ) -> list:
    query = """
    SELECT books.title,
        STRING_AGG (
            users.first_name || ' ' || users.last_name, ','
            ORDER BY users.first_name, users.last_name
        ) patrons,
        checked_out.borrowed_date,
        checked_out.fees_due

        FROM library.checked_out
        INNER JOIN library.book_copies USING (book_copy_id)
        INNER JOIN library.books USING (book_id)
        INNER JOIN library.users USING (user_id)
        INNER JOIN library.locations USING (location_id)
        WHERE ( library.checked_out.fees_due > 0.0
        AND locations.location_id=%s)
        GROUP BY book_copies.book_copy_id,
                books.title,
                checked_out.borrowed_date, checked_out.fees_due
        ORDER BY checked_out.borrowed_date ASC
    """
    result = exec_get_all(query, (location_id,) )
    return result

"""
Returns a list of all the reserved books
"""
def get_all_reserved() -> list:
    query = """
    SELECT books.title
    FROM library.books
    INNER JOIN library.reserved
    ON reserved.book_id = books.book_id
    """
    result = exec_get_all(query, )
    result = [element for list in result for element in list if element != None]
    return result

"""
Returns a list of all books checked out including their title, authors, genre,
the user whose borrowing them, the date checked out, and the date returned
"""
def get_checkout_log() -> list:
    query = """
    SELECT books.title,
        STRING_AGG (
                authors.first_name || ' ' || authors.last_name, ','
                ORDER BY authors.first_name, authors.last_name
            ) book_authors,
        books.genre,
        STRING_AGG (
            users.first_name || ' ' || users.last_name, ','
            ORDER BY users.first_name, users.last_name
        ) patrons,

        checked_out.borrowed_date, checked_out.returned_date
        FROM library.books
        INNER JOIN library.wrote USING (book_id)
        INNER JOIN library.authors USING (author_id)
        INNER JOIN library.book_copies USING (book_id)
        INNER JOIN library.checked_out USING (book_copy_id)
        INNER JOIN library.users USING (user_id)
        GROUP BY books.title, books.genre,
            users.first_name, users.last_name,
            checked_out.borrowed_date, checked_out.returned_date
        ORDER BY books.genre, book_authors ASC
    """

    result = exec_get_all(query, )
    return result

"""
Returns a list of a book's author given the book_id
"""
def get_book_authors(book_id) -> list:
    query = """
    SELECT first_name, middle_name, last_name
    FROM library.authors
    INNER JOIN library.wrote
    ON authors.author_id = wrote.author_id
    WHERE book_id=%s
    """
    return exec_get_all(query, (book_id,))

"""
Return true if a book is checked out and false
otherwise
"""
def is_checked_out(book_copy_id) -> bool:
    query = """
    SELECT book_copies.is_checked_out
    FROM library.book_copies
    WHERE book_copies.book_copy_id=%s
    """
    result = exec_get_all(query, (book_copy_id,))
    return result[0][0]

"""
Given a book_id returns a list of all book copies not
checked out
"""
def search_for_available_book_copies(book_id) -> list:
    query = """
    SELECT book_copies.book_copy_id,
    (
        (SELECT COUNT(book_copies.book_id)
        FROM library.book_copies
        WHERE book_id=%s
        )
        -
        (SELECT COUNT(book_copies.book_id)
        FROM library.book_copies
        WHERE is_checked_out = true
        AND book_id=%s
        )
    ) AS available_copies,
    book_copies.location_id
    FROM library.book_copies
    WHERE library.book_copies.book_id=%s
    AND library.book_copies.is_checked_out = false
    """
    result = exec_get_all(query, (book_id, book_id, book_id, ))
    return result

"""
Returns a list of all registered authors and their names
"""
def get_all_authors() -> list:
    query = """SELECT first_name, middle_name, last_name FROM library.authors"""
    result = exec_get_all(query)
    return result

"""
Returns a list of all registered books with their title and authors
"""
def get_all_books() -> list:
    query = """
    SELECT b.title,
        STRING_AGG (
            a.first_name || ' ' || a.last_name, ','
            ORDER BY a.first_name, a.last_name
        ) author_list
    FROM library.books b
    INNER JOIN library.wrote w USING (book_id)
    INNER JOIN library.authors a USING (author_id)
    GROUP BY b.title
    """
    result = exec_get_all(query, )
    return result

"""
Returns a list of all the users' names
"""
def get_all_users() -> list:
    query = """
    SELECT users.first_name, users.middle_name, users.last_name
    FROM library.users
    """
    result = exec_get_all(query)
    return result

"""
Returns a list of all the books a user has checked out including
the title and book_copy_id
"""
def get_checked_out(user_id) -> list:
    query = """
            SELECT books.title,
            book_copies.book_copy_id
            FROM library.checked_out
            INNER JOIN library.users USING (user_id)
            INNER JOIN library.book_copies USING (book_copy_id)
            INNER JOIN library.books USING (book_id)
            WHERE users.user_id=%s
            ORDER BY books.title ASC
            """
    result = exec_get_all(query, (user_id,))
    result = [element for list in result for element in list if element != None]
    
    return result

"""
COUNT GETTERS
"""
"""
Calculates the time the book copy has been checked out given the current
date and a checked_out_id. Returns the number of days the book has been borrowed
"""
def get_days_borrowed(checked_out_id, current_date) -> int:
    query = """
    SELECT EXTRACT(day from
        %s
        -
        (
        SELECT borrowed_date
        FROM library.checked_out
        WHERE library.checked_out.checked_out_id=%s
        )::timestamp
    ) AS days_borrowed
    """
    result = exec_get_all(query, (current_date, checked_out_id))
    days_borrowed = int(result[0][0])
    return days_borrowed

"""
Calculates the time the book copy has been checked out given a checked_out_id. 
Returns the number of days the book has been borrowed based on when it was returned
"""
def get_days_borrowed_after_returned(checked_out_id) -> int:
    query = """
    SELECT EXTRACT(day from
        (
        SELECT returned_date
        FROM library.checked_out
        WHERE library.checked_out.checked_out_id=%s
        )::timestamp
        -
        (
        SELECT borrowed_date
        FROM library.checked_out
        WHERE library.checked_out.checked_out_id=%s
        )::timestamp
    ) AS days_borrowed
    """
    result = exec_get_all(query, (checked_out_id, checked_out_id))
    days = int(result[0][0])
    return days

# Gets the total num of copies for a book at all locations
def get_total_num_book_copies(book_id) -> int:
    query = """
        SELECT COUNT(book_copies.book_id)
        FROM library.book_copies
        WHERE library.book_copies.book_id=%s
        """
    result = exec_get_all(query, (book_id, ))
    count = result[0][0]
    return count

# Gets the total num of copies for a book at a specific location
def get_total_num_book_copies_at_location(book_id, location_id) -> int:
    query = """
        SELECT COUNT(book_copies.book_id)
        FROM library.book_copies
        INNER JOIN library.locations
        ON locations.location_id = book_copies.location_id
        WHERE library.book_copies.book_id=%s
        AND library.locations.location_id=%s
        """
    result = exec_get_all(query, (book_id, location_id))
    count = result[0][0]
    return count

"""
RECORD GETTERS
"""
# Given a book id returns the book's title and authors
def get_book(book_id) -> list:
    query = """
    SELECT books.title,
        STRING_AGG (
            authors.first_name || ' ' || authors.last_name, ','
            ORDER BY authors.first_name, authors.last_name
        ) author_list
    FROM library.books
    INNER JOIN library.wrote
    ON library.books.book_id = library.wrote.book_id
    INNER JOIN library.authors 
    ON library.authors.author_id = library.wrote.author_id
    WHERE books.book_id=%s
    GROUP BY books.title
    """
    return exec_get_all(query, (book_id,))

# Given an author id returns the author's name
def get_author(author_id) -> list:
    query = """
    SELECT first_name, middle_name, last_name
    FROM library.authors
    WHERE authors.author_id=%s
    """
    return exec_get_all(query, author_id,)

"""
COLUMN GETTERS
"""
# Returns the title of all books with the given genre
def get_all_of_genre(genre) -> list:
    query = """
        SELECT books.title FROM library.books
        WHERE genre=%s
        """
    result = exec_get_all(query, (genre,))
    result = [element for list in result for element in list if element != None]
    quantity = len(result)
    return result, quantity

# Given a single checkout ID, returns the fees due
def get_fees_due(checkout_id : int) -> float:
    query = """
        SELECT fees_due FROM library.checked_out
        WHERE checked_out.checked_out_id=%s
        """
    result = exec_get_all(query, (checkout_id, ))
    fee = result[0][0]
    return fee

# Given a list of checkout ID, returns the sum of all the fee_due
def get_all_fees_due(checkout_ids : list) -> float:
    total_fees = 0.0

    for id in checkout_ids:
        total_fees += get_fees_due(id)

    return total_fees

"""
ID GETTERS
"""
"""
Returns a single book_copy_id that isn't checked out for any location
"""
def get_one_book_copy(book_id) -> int:
    result = search_for_available_book_copies(book_id)
    if (result == []):
        return "No copies available!"
    copy_id = result[0][0]
    return copy_id

"""
Returns a single book_copy_id that isn't checked out for a specific location
"""
def get_one_book_copy_at_location(book_id, location_id) -> int:
    result = search_for_available_book_copies(book_id)
    if (result == []):
        return "No copies available!"

    for copy in result:
        location = copy[2]
        if location == location_id:
            copy_id = copy[0]
            return copy_id

    return "No copies found with the given location ID."

"""
Returns a list of all the checkouts a user has made
and their ids
"""
def get_all_checked_out_ids(user_id) -> list:
    query = """
            SELECT checked_out.checked_out_id
            FROM library.checked_out
            INNER JOIN library.users USING (user_id)
            WHERE users.user_id=%s
            """
    result = exec_get_all(query, (user_id,))
    result = [element for list in result for element in list if element != None]
    
    return result

"""
Returns a list of ids for all the users in the database
"""
def get_all_users_ids() -> list:
    query = """
    SELECT users.user_id
    FROM library.users
    """
    result = exec_get_all(query)
    result = [element for list in result for element in list if element != None]
    return result

def get_checked_out_id(user_id, book_copy_id, borrowed_date) -> int:
    try:
        query = """
        SELECT checked_out_id
        FROM library.checked_out
        WHERE user_id=%s AND book_copy_id=%s AND borrowed_date=%s
        """
        result = exec_get_all(query, (user_id, book_copy_id, borrowed_date))
        return result[0][0]
    except IndexError:
        return "Checkout not found."

def get_user_id(first_name, middle_name, last_name, email, phone) -> int:
    try:
        query = """
        SELECT users.user_id FROM library.users
        WHERE first_name=%s AND (middle_name=%s OR middle_name IS NULL)
        AND last_name=%s AND email=%s AND phone=%s
        """
        result = exec_get_all(query, (first_name, middle_name, last_name, email, phone))
        return result[0][0]
    except IndexError:
        return "User does not exist. Please create an account."

def get_book_id(title, genre, sub_genre, summary, publish_date) -> int:
    try:
        query = """
        SELECT books.book_id
        FROM library.books
        WHERE title=%s AND genre=%s AND sub_genre=%s AND summary=%s
        AND publish_date=%s
        """
        result = exec_get_all(query, (title, genre, sub_genre, summary, publish_date))
        return result[0][0]
    except IndexError:
        return "Book not registered."

def get_author_id(first_name, middle_name, last_name) -> int:
    try:
        query = """
        SELECT authors.author_id
        FROM library.authors
        WHERE first_name=%s AND (middle_name=%s OR middle_name IS NULL)
        AND last_name=%s
        """
        result = exec_get_all(query, (first_name, middle_name, last_name))
        return result[0][0]
    except IndexError:
        return "Author not registered"