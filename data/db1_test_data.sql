INSERT INTO library.locations (location_id, title, "address", phone)
    VALUES
    (1, 'Pittsford Community Library', '24 State St, Pittsford, NY 14534','(585) 248-6275'),
    (2, 'Henrietta Public Library', '625 Calkins Rd, Rochester, NY 14623', '(585) 359-7092'),
    (3, 'Fairport Public Library', '1 Fairport Village Landing, Fairport, NY 14450','(585) 223-9091'),
    (4,'Penfield Public Library', '1985 Baird Rd, Penfield, NY 14526', '(585) 340-8720');

INSERT INTO library.authors (author_id ,first_name, middle_name, last_name)
    VALUES
    (1, 'Henry', 'David', 'Thoreau'),
    (2, 'Charles', NULL, 'Darwin'),
    (3, 'Benjamin', NULL, 'Franklin'),
    (4, 'Harper', NULL, 'Lee'),
    (5, 'Jerome', 'David', 'Salinger'),
    (6, 'Bob', 'Lloyd', 'Evans'),
    (7, 'Jane', 'Mary', 'Smith');

INSERT INTO library.books (sub_genre, summary, book_id, title, genre, publish_date)
    VALUES
    ('memoir', 'This is a book', 1, 'Walden', 'non-fiction', '1854-08-09'),
    ('YA', 'This is a book', 2, 'The Autobiography of Charles Darwin', 'non-fiction', '1887-05-13'),
    ('YA', 'This is a book', 3, 'The Autobiography of Benjamin Franklin', 'non-fiction', '1791-03-06'),
    ('YA', 'This is a book', 4, 'To Kill a Mockingbird', 'fiction', '1960-07-11'),
    ('YA', 'This is a book', 5, 'Go Set a Watchman', 'fiction', '2015-07-14'),
    ('young adult', 'This is a book', 6, 'The Catcher in the Rye', 'fiction', '1951-07-16');

INSERT INTO library.wrote (author_id, book_id)
    VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (4, 5),
    (5, 6),
    (6, 6),
    (7, 6);

INSERT INTO library.book_copies (book_id, location_id)
    VALUES
	(1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), -- 1-7
	(2, 1), (2, 1), (2, 1), -- 8-10
	(3, 1), (3, 1), (3, 1), -- 11-13
	(4, 1), (4, 1), (4, 1), (4, 1), (4, 1), (4, 1), (4, 1), (4, 1), (4, 1), (4, 1), -- 14-23
	(5, 1), (5, 1), (5, 1), (5, 1), (5, 1), -- 24-28
	(6, 1), (6, 1), (6, 1); -- 29-31

INSERT INTO library.users (user_id, first_name, middle_name, last_name, email, phone)
    VALUES
    (1, 'Ada', NULL, 'Lovelace', 'lovelace321@gmail.com', '020-321-1029'),
    (2, 'Mary', NULL, 'Shelley', 'mary453shell@gmail.com', '020-829-1023'),
    (3, 'Jackie', NULL, 'Gleason', 'johngleason9870@gmail.com', '718-482-0234'),
    (4, 'Art', NULL, 'Garfunkel', 'art0123@gmail.com',  '347-423-5567');

INSERT INTO library.checked_out (user_id, book_copy_id, borrowed_date) 
    VALUES
    (1, 1, '2022-07-11'), (1, 8, '2022-07-11'), (1, 11, '2022-07-11'), (1, 14, '2022-07-11'), (1, 24, '2022-07-11'), (1, 29, '2022-07-11'),
    (2, 2, '2022-07-11'), (2, 9, '2022-07-11'), (2, 12, '2022-07-11'), (2, 15, '2022-07-11'),
    (3, 30, '2022-07-11'), (3, 28, '2022-07-11'), (3, 23, '2022-07-11');