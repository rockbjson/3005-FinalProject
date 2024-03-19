-- Ashley Fong
-- 101226835
-- COMP3005 Assignment 2
-- 26 February 2024

-- a.  
SELECT title from Books; 

-- b.  
SELECT first_name, last_name
FROM members
WHERE join_date > '2023-01-01';

-- c. 
SELECT first_name, last_name, COUNT(borrowing.member_id) AS borrowCount
FROM members
FULL OUTER JOIN borrowing 
ON members.member_id = borrowing.member_id 
GROUP BY first_name, last_name
ORDER BY borrowCount DESC;

-- d. 
SELECT first_name, last_name
FROM authors, books
WHERE authors.author_id = books.author_id
GROUP BY authors.author_id, first_name, last_name
HAVING COUNT(books.book_id) > 1;

-- e. 
SELECT first_name, last_name
FROM members
WHERE member_id NOT IN (
	SELECT member_id 
	FROM borrowing
);

-- f. 
SELECT title, published_date
FROM books
ORDER BY published_date DESC
LIMIT 1;

-- g. 
SELECT publisher_name, COUNT(books.publisher_id) as countBooks
FROM publishers, books
WHERE publishers.publisher_id = books.publisher_id
GROUP BY publisher_name, publishers.publisher_id, books.publisher_id
ORDER BY countBooks DESC;

-- h.
SELECT title
FROM books, borrowing
WHERE books.book_id = borrowing.book_id AND borrow_date = NULL;

-- i.
SELECT DISTINCT members.first_name, members.last_name
FROM members, borrowing, books, authors
WHERE members.member_id = borrowing.member_id AND 
	borrowing.book_id = books.book_id AND
	books.author_id = authors.author_id AND
	authors.first_name = 'J.K.' AND authors.last_name = 'Rowling';

-- j. 
SELECT authors.first_name, authors.last_name
FROM authors, books, borrowing 
WHERE authors.author_id = books.author_id AND 
	books.book_id = borrowing.book_id
GROUP BY authors.first_name, authors.last_name, authors.author_id, borrowing.borrow_id
HAVING COUNT(borrow_id) > 3;

