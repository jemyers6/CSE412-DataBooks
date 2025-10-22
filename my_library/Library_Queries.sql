/*
 This query joins the book_genre and genres tables
 and counts the number of books for each genre
*/
SELECT genres.genre_name, COUNT(book_genre.isbn) AS number_of_books
FROM book_genre
JOIN genres ON book_genre.genre_id = genres.genre_id
GROUP BY genres.genre_name;

-- Query to calculate the total price of all books
SELECT SUM(list_price_usd) AS total_price FROM books;

-- SQL query to count the number of books for each author
SELECT author, COUNT(*) AS number_of_books 
FROM books 
GROUP BY author
ORDER BY number_of_books DESC;

--To add a book to your database, you will use an INSERT INTO SQL statement. Here's a generic SQL query template you can use:

INSERT INTO books (isbn, title, author, genre, editor, publication_year, edition, list_price_usd, rating, citation)
VALUES ('ISBN_Value', 'Title_Value', 'Author_Value', 'Genre_Value', 'Editor_Value', PublicationYear_Value, 'Edition_Value', ListPriceUSD_Value, Rating_Value, 'Citation_Value');

--To add a book to your database, you will use an INSERT INTO SQL statement. 
INSERT INTO books (isbn, title, author, genre, editor, publication_year, edition, list_price_usd, rating, citation)
VALUES ('1234567890', 'Example Book Title', 'John Doe', 'Fiction', 'Jane Smith', 2021, '1st', 19.99, 4.5, 'Doe, J. (2021). Example Book Title. 1st ed. Edited by Jane Smith.');

--Here's a generic SQL query template to delete a book based on its ISBN:
DELETE FROM books WHERE isbn = 'ISBN_Value';
--Replace ISBN_Value with the actual ISBN of the book you wish to delete. For example:
DELETE FROM books WHERE isbn = '1234567890';

--To modify an existing record in your database, you would use an UPDATE SQL statement. 
UPDATE books
SET column_name = 'New_Value'
WHERE isbn = 'Specific_ISBN';

--For example, to update the title of a book:
UPDATE books
SET title = 'New Book Title'
WHERE isbn = '1234567890';

--To display the top 3 books with the best ratings from your database, you can use a SQL query with an ORDER BY clause and a LIMIT
SELECT title, rating
FROM books
ORDER BY rating DESC
LIMIT 3;

--To classify books into intervals based on their ratings, you can use a SQL query with a CASE statement
SELECT title, 
       rating,
       CASE 
         WHEN rating >= 4.5 THEN 'Excellent'
         WHEN rating >= 3.5 AND rating < 4.5 THEN 'Good'
         WHEN rating >= 2.5 AND rating < 3.5 THEN 'Average'
         WHEN rating >= 1.5 AND rating < 2.5 THEN 'Below Average'
         ELSE 'Poor'
       END AS rating_category
FROM books
ORDER BY rating DESC;

/*To find the oldest and the newest book in your database, 
you can use two SQL queries, each with an ORDER BY clause based 
on the publication_year column and a LIMIT 1 to get only one record.*/

--For the Oldest Book:
SELECT title, publication_year
FROM books
ORDER BY publication_year ASC
LIMIT 1;

--For the Newest Book:
SELECT title, publication_year
FROM books
ORDER BY publication_year DESC
LIMIT 1;

--To insert a new column in the books table to record the number of pages of each book, you would use an SQL ALTER TABLE statement:
ALTER TABLE books
ADD COLUMN number_of_pages INTEGER;

-- to calculate the total number of pages of all the books in your books table, you can use an SQL SELECT statement with the SUM function.
SELECT SUM(number_of_pages) AS total_pages
FROM books;

--To get the number of pages by genre, you need to join the books table with the book_genre and genres tables. This will allow you to group the results by genre and sum up the number of pages for each genre.
SELECT g.genre_name, SUM(b.number_of_pages) AS total_pages
FROM books b
JOIN book_genre bg ON b.isbn = bg.isbn
JOIN genres g ON bg.genre_id = g.genre_id
GROUP BY g.genre_name
ORDER BY total_pages DESC;

--Add a New Column for Language: First, you'll need to add a new column to your books table to store the language information.
ALTER TABLE books
ADD COLUMN language VARCHAR(50);

--Add a New Column for Printing location: First, you'll need to add a new column to your books table to store the printing location information.
ALTER TABLE books
ADD COLUMN printing_location VARCHAR(50);

--To count the number of books by language in your SQL database, you can use a SELECT statement with the COUNT function and a GROUP BY clause. 

SELECT language, COUNT(*) AS number_of_books
FROM books
GROUP BY language
ORDER BY number_of_books DESC;

--To retrieve the top five editors based on the number of books they have edited in your database, you can use an SQL query that counts the number of books associated with each editor and then orders the results to get the top five.
SELECT editor, COUNT(*) AS number_of_books
FROM books
GROUP BY editor
ORDER BY number_of_books DESC
LIMIT 5;

--To retrieve the number of books by their edition from your database, you can use a SQL query with the COUNT function and a GROUP BY clause.

SELECT edition, COUNT(*) AS number_of_books
FROM books
GROUP BY edition
ORDER BY number_of_books DESC;

--To find out how many books you have for each publication year in your database, you can use a SQL query that groups the books by their publication year and then counts the number of books in each group.
SELECT publication_year, COUNT(*) AS number_of_books
FROM books
GROUP BY publication_year
ORDER BY number_of_books DESC;




