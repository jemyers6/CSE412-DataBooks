CREATE TABLE Author (
	author_id INT PRIMARY KEY,
	name VARCHAR(100),
	avg_rating DECIMAL(3,2)
);

CREATE TABLE Book (
	ISBN CHAR(13) PRIMARY KEY,
	title VARCHAR(200) NOT NULL,
	edition VARCHAR(20),
	list_price DECIMAL(8,2),
	publicationyear INT,
	editor VARCHAR(100),
	avg_rating DECIMAL (3,2),
	num_pages INT,
	lang VARCHAR(50),
	citation TEXT 
);

CREATE TABLE Writes (
	author_id INT NOT NULL,
	ISBN CHAR(13) NOT NULL,
	PRIMARY KEY (author_id, ISBN),
	FOREIGN KEY (author_id) REFERENCES Author(author_id) ON DELETE CASCADE,
	FOREIGN KEY (ISBN) REFERENCES Book(ISBN) ON DELETE CASCADE
);

CREATE TABLE DigitalShelf (
	shelf_id INT PRIMARY KEY,
	shelf_type VARCHAR(50),
	name VARCHAR(100)
);

CREATE TABLE AddedToShelf (
	shelf_id INT NOT NULL,
	ISBN CHAR(13) NOT NULL,
	PRIMARY KEY (shelf_id, ISBN),
	FOREIGN KEY (shelf_id) REFERENCES DigitalShelf(shelf_id) ON DELETE CASCADE,
	FOREIGN KEY (ISBN) REFERENCES Book(ISBN) ON DELETE CASCADE
);

CREATE TABLE PersonalRating (
	ISBN CHAR(13) PRIMARY KEY,
	rating INT check (rating BETWEEN 1 AND 5)
	text_review VARCHAR(1000),
	FOREIGN KEY (ISBN) REFERENCES Book(ISBN) ON DELETE CASCADE
);

CREATE TABLE BookStatus (
	ISBN CHAR(13) PRIMARY KEY,
	progress_page INT CHECK (progress_page >= 0),
	read_status VARCHAR(20) CHECK (read_status IN ('WANT_TO_READ', 'CURRENTLY_READING', 'READ')),
	updated_at VARCHAR(50) NULL,
	start_date VARCHAR(50),
	finish_date VARCHAR(50),
	FOREIGN KEY (ISBN) REFERENCES Book(ISBN) ON DELETE CASCADE
);


