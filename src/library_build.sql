DROP SCHEMA IF EXISTS library CASCADE;
DROP TABLE IF EXISTS library.locations CASCADE;
DROP TABLE IF EXISTS library.reserved CASCADE;
DROP TABLE IF EXISTS library.checked_out CASCADE;
DROP TABLE IF EXISTS library.users CASCADE;
DROP TABLE IF EXISTS library.book_copies CASCADE;
DROP TABLE IF EXISTS library.books CASCADE;
DROP TABLE IF EXISTS library.wrote CASCADE;
DROP TABLE IF EXISTS library.authors CASCADE;

CREATE SCHEMA library;

CREATE TABLE library.locations (
    location_id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    "address" text NOT NULL,
    phone varchar(15) NOT NULL
);

CREATE TABLE library.authors (
    author_id SERIAL NOT NULL PRIMARY KEY,
    first_name text NOT NULL,
    middle_name text,
    last_name text NOT NULL
);

CREATE TABLE library.books (
    book_id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    genre text NOT NULL,
    sub_genre text,
    summary text NOT NULL,
    publish_date date NOT NULL
);

CREATE TABLE library.wrote (
    author_id integer NOT NULL,
    book_id integer NOT NULL,
    CONSTRAINT author_id
        FOREIGN KEY(author_id)
        REFERENCES library.authors(author_id),
    CONSTRAINT book_id
        FOREIGN KEY(book_id)
        REFERENCES library.books(book_id)
);

CREATE TABLE library.book_copies (
    book_copy_id SERIAL NOT NULL PRIMARY KEY,
    book_id integer NOT NULL,
    is_checked_out boolean DEFAULT false NOT NULL,
    location_id integer NOT NULL,
    CONSTRAINT book_id
        FOREIGN KEY(book_id)
        REFERENCES library.books(book_id),
    CONSTRAINT location_id
        FOREIGN KEY(location_id)
        REFERENCES library.locations(location_id)
);

CREATE TABLE library.users (
    user_id SERIAL NOT NULL PRIMARY KEY,
    first_name text NOT NULL,
    middle_name text,
    last_name text NOT NULL,
    email text NOT NULL,
    phone varchar(15) NOT NULL,
    is_locked boolean DEFAULT false NOT NULL
    -- ON DELETE CASCADE
);

CREATE TABLE library.reserved (
    reserved_id SERIAL NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    book_id integer NOT NULL,
    CONSTRAINT user_id
        FOREIGN KEY(user_id)
        REFERENCES library.users(user_id),
    CONSTRAINT book_id
        FOREIGN KEY(book_id)
        REFERENCES library.books(book_id)
);

CREATE TABLE library.checked_out (
    checked_out_id SERIAL NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    book_copy_id integer NOT NULL,
    borrowed_date date NOT NULL,
    returned_date date, --if NOT NULL, the book has been returned
    due_date date, 
    fees_due float default 0.0 NOT NULL,
    days_borrowed integer,
    CONSTRAINT user_id
        FOREIGN KEY(user_id)
        REFERENCES library.users(user_id),
    CONSTRAINT book_copy_id
        FOREIGN KEY(book_copy_id)
        REFERENCES library.book_copies(book_copy_id)
);

-- When a book is checked_out a due date is set for 14 days later.
CREATE OR REPLACE FUNCTION set_due_date()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN

    UPDATE library.checked_out
        SET due_date = (
            borrowed_date + (14 || ' days')::interval
        );

	RETURN NEW;
END;
$$;

CREATE TRIGGER book_copy_is_checked_out
  AFTER INSERT
  ON library.checked_out
  FOR EACH ROW
  EXECUTE PROCEDURE set_due_date();

-- When a book is returned calculate the number of days borrowed.
CREATE OR REPLACE FUNCTION count_days_borrowed()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN

    UPDATE library.checked_out
        SET days_borrowed = (
            SELECT EXTRACT (day from
                (returned_date)::timestamp
                    -
                (borrowed_date)::timestamp
            ) AS days_borrowed
        );

	RETURN NEW;
END;
$$;

CREATE TRIGGER book_copy_is_returned
  AFTER UPDATE OF returned_date
  ON library.checked_out
  FOR EACH ROW
  EXECUTE PROCEDURE count_days_borrowed();