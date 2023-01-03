INSERT INTO library.locations (location_id, title, "address", phone)
    VALUES
    (1, 'Pittsford Community Library', '24 State St, Pittsford, NY 14534','(585) 248-6275'),
    (2, 'Henrietta Public Library', '625 Calkins Rd, Rochester, NY 14623', '(585) 359-7092'),
    (3, 'Fairport Public Library', '1 Fairport Village Landing, Fairport, NY 14450','(585) 223-9091'),
    (4,'Penfield Public Library', '1985 Baird Rd, Penfield, NY 14526', '(585) 340-8720');

INSERT INTO library.users (user_id, first_name, middle_name, last_name, email, phone)
    VALUES
    (1, 'Ada', NULL, 'Lovelace', 'lovelace321@gmail.com', '020-321-1029'),
    (2, 'Mary', NULL, 'Shelley', 'mary453shell@gmail.com', '020-829-1023'),
    (3, 'Jackie', NULL, 'Gleason', 'johngleason9870@gmail.com', '718-482-0234'),
    (4, 'Art', NULL, 'Garfunkel', 'art0123@gmail.com',  '347-423-5567');

INSERT INTO library.books(title, summary, genre, sub_genre, publish_date, book_id)
  VALUES
  ('A Hitchhikers Guide to the Galaxy', 'Don''t panic', 'Fiction', 'Science Fiction',
  '1979-10-12', 1),
  ('The Invisible Man', 'Life is to be lived not controlled', 'Fiction', 'Literature',
  '1952-04-14', 2),
  ('To Kill a Mockingbird', 'Explores themes of racial prejudice and injustice', 'Fiction',
  'Coming-of-age', '1960-07-11', 3),
  ('Go Set a Watchman', 'A sequel featuring Scout returnng to visit her father', 'Fiction',
  'Historical Fiction', '2015-07-14', 4),
  ('The Catcher in the Rye', 'A critique of superficiality in society', 'Fiction', 'Coming-of-age story',
  '1951-07-16', 5),
  ('Good Omens', 'The Nice and Accurate Prophecies of Agnes Nutter', 'Fiction', 'Humor',
  '1990-05-10', 6);

INSERT INTO library.authors(author_id, first_name, middle_name, last_name)
  VALUES
  (1, 'Douglas', NUll, 'Adams'),
  (2, 'Ralph', NULL, 'Ellison'),
  (3, 'Harper', NULL, 'Lee'),
  (4, 'Jerome', 'David', 'Salinger'),
  (5, 'Terry', NULL, 'Pratchett'),
  (6, 'Neil', NULL, 'Gaiman');

INSERT INTO library.wrote(author_id, book_id)
  VALUES
  (1, 1),
  (2, 2),
  (3, 3),
  (3, 4),
  (4, 5),
  (5, 6),
  (6, 6);

--BOOK 1
DO $FN$
BEGIN
    FOR counter IN 1..42 LOOP
        EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
            VALUES (1, 1) $$
            USING counter;
    END LOOP;
END;
$FN$;

DO $FN$
BEGIN
  FOR counter IN 1..2 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (1, 2); $$
        USING counter;
  END LOOP;
END;
$FN$;

--BOOK 2
DO $FN$
BEGIN
  FOR counter IN 1..5 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (2, 4); $$
        USING counter;
  END LOOP;
END;
$FN$;

--BOOK 3
DO $FN$
BEGIN
  FOR counter IN 1..2 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (3, 1); $$
        USING counter;
  END LOOP;
END;
$FN$;

DO $FN$
BEGIN
  FOR counter IN 1..7 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (3, 2); $$
        USING counter;
  END LOOP;
END;
$FN$;

DO $FN$
BEGIN
  FOR counter IN 1..3 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (3, 3); $$
        USING counter;
  END LOOP;
END;
$FN$;

--BOOK 4
DO $FN$
BEGIN
  FOR counter IN 1..7 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (4, 4); $$
        USING counter;
  END LOOP;
END;
$FN$;

--BOOK 5
DO $FN$
BEGIN
  FOR counter IN 1..3 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (5, 3); $$
        USING counter;
  END LOOP;
END;
$FN$;

--BOOK 1
DO $FN$
BEGIN
    FOR counter IN 1..6 LOOP
        EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
            VALUES (6, 2) $$
            USING counter;
    END LOOP;
END;
$FN$;