import psycopg2
import datetime
from datetime import date

# may need to change this based on your local database name
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="booksdb",
    user="carissa"
)

cursor = conn.cursor()

def main():
    cursor.execute("SELECT COUNT(*) FROM Book;")
    count = cursor.fetchone()[0]
    print("Books in DB:", count)
    print("Welcome to DataBooks!")
    while True:
        print("\nChoose an option below:")
        print("a. Add Book to shelf")
        print("b. Create a new shelf")
        print("c. Update status of a book")
        print("d. Delete a bookshelf")
        print("e. Create a review for a book")
        print("f. Remove book from a shelf")
        print("g. Show all books by personal ratings")
        print("h. Show books from author")
        print("i. Show currently reading")
        print("j. Show want to read")
        print("k. Show bookshelf with the most amount of books")
        print("q. Leave Databooks")

        choice = input("Enter choice: ").lower().strip()

        if choice == 'a':
            add_to_shelf()

        elif choice == 'b':
            create_shelf()

        elif choice == 'c':
            update_status()

        elif choice == 'd':
            delete_bookshelf()

        elif choice == 'e':
            create_review()

        elif choice == 'f':
            remove_from_shelf()

        elif choice == 'g':
            show_by_rating()

        elif choice == 'h':
            show_by_author()

        elif choice == 'i':
            show_currently_reading()

        elif choice == 'j':
            show_want_to_read()

        elif choice == 'k':
            show_bookshelf_most()

        elif choice == 'q':
            print("Thank you for using DataBooks!")
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Try again.")

# a
def add_to_shelf(): # INSERT INTO AddedToShelf (shelf_id, ISBN)
    shelf_name = input("Enter shelf Name: ")
    book_name = input("Enter book name: ")
    author_name = input("Enter author name: ")

    cursor.execute("""
        SELECT shelf_id
        FROM DigitalShelf
        WHERE name = %s
        """, (shelf_name,))
    shelf = cursor.fetchone()

    if not shelf:
        print("Shelf not found")
        return

    shelf_id = shelf[0]

    cursor.execute("""
        SELECT b.isbn 
        FROM Book b 
        JOIN Writes w ON b.isbn = w.isbn 
        JOIN Author a ON w.author_id = a.author_id 
        WHERE b.title = %s AND a.name = %s
        """, (book_name, author_name))

    book = cursor.fetchone()

    if not book:
        print("Book not found, check title and author.")
        return

    isbn = book[0]

    cursor.execute("""
        SELECT 1 FROM AddedToShelf
        WHERE shelf_id = %s AND isbn = %s
        """, (shelf_id, isbn))

    if cursor.fetchone():
        print("Book is already in shelf")
        return

    cursor.execute("""
        INSERT INTO AddedToShelf (shelf_id, isbn)
        VALUES (%s, %s)
        """, (shelf_id, isbn))

    conn.commit()

    print("Book successfully added to shelf!")

# b
def create_shelf(): # INSERT INTO DigitalShelf (shelf_id, name, shelf_type)
    # INSERT INTO DigitalShelf (shelf_id, name, shelf_type)
    #   VALUES (11, 'Dark Academia','OTHER');
    shelf_name = input("Enter name of new shelf: ")
    shelf_type = input("Enter type of new shelf: ")
    # get shelf id as the next num in number of shelves
    cursor.execute("SELECT COUNT(*) FROM DigitalShelf")
    count = cursor.fetchone()[0] + 1

    cursor.execute("""
        SELECT shelf_id
        FROM DigitalShelf
        WHERE name = %s
        """, (shelf_name,))

    shelf = cursor.fetchone()
    if shelf:
        print("Shelf already exists!")
        return

    cursor.execute("""
        INSERT INTO DigitalShelf (shelf_id, name, shelf_type)
                   VALUES (%s, %s, %s)
                   """, (count, shelf_name, shelf_type))

    conn.commit()

    print("Shelf successfully created")

# c
def update_status(): # UPDATE BookStatus
    # UPDATE BookStatus
    # SET
    # read_status = 'READ', – Can also be 'CURRENTLY_READING' or 'WANT_TO_READ'
    # progress_page = 270, – assumes full progress
    # finish_date = '2025-10-22',
    # updated_at = CURRENT_TIMESTAMP
    # WHERE ISBN = '9781984854032';

    book_name = input("Enter book name: ")
    author_name = input("Enter author name: ")
    progress_page = input("Enter current page: ")
    new_status = input("Enter updated status: ")
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    cur_date = f"{year}-{month}-{day}"

    cursor.execute("""
        SELECT b.isbn
        FROM Book b
        JOIN Writes w ON b.isbn = w.isbn 
        JOIN Author a ON w.author_id = a.author_id
        WHERE b.title = %s AND a.name = %s
        """, (book_name, author_name))

    book = cursor.fetchone()

    if not book:
        print("Book not found, check title and author.")
        return

    isbn = book[0]

    print("Updating status...")
    if not new_status == "READ":
        cursor.execute("""
            UPDATE BookStatus
            SET read_status = %s,
                progress_page = %s,
                finish_date = NULL,
                updated_at = %s
            WHERE ISBN = %s
            """, (new_status, progress_page, cur_date, isbn))
    else:
        cursor.execute("""
                       UPDATE BookStatus
                       SET read_status   = %s,
                           progress_page = %s,
                           finish_date   = %s,
                           updated_at    = %s
                       WHERE ISBN = %s
                       """, (new_status, progress_page, cur_date, cur_date, isbn))

    conn.commit()

    print(f"Book {book_name} status successfully to {new_status}")



# d
def delete_bookshelf(): # DELETE FROM DigitalShelf
    # DELETE FROM DigitalShelf
    # WHERE shelf_id = 1;
    shelf_name = input("Enter bookshelf Name: ")

    cursor.execute("""
        SELECT shelf_id
        FROM DigitalShelf
        WHERE name = %s
        """, (shelf_name,))

    shelf = cursor.fetchone()

    if not shelf:
        print("Shelf not found")
        return

    shelf_id = shelf[0]

    print("Deleting bookshelf...")
    cursor.execute("""
        DELETE FROM DigitalShelf
        WHERE shelf_id = %s
        """, (shelf_id,))

    conn.commit()

    print("Bookshelf successfully deleted")

# e
def create_review(): # INSERT INTO PersonalRating (ISBN, rating, text_review)
    book_name = input("Enter book name: ")
    author_name = input("Enter author name: ")
    rating = input("Enter rating from 1-5: ")
    review = input("Enter review: ")

    cursor.execute("""
        SELECT b.isbn
        FROM Book b 
        JOIN Writes w ON b.isbn = w.isbn
        JOIN Author a ON w.author_id = a.author_id
        WHERE b.title = %s AND a.name = %s
        """, (book_name, author_name))

    book = cursor.fetchone()

    if not book:
        print("Book not found, check title and author.")
        return

    isbn = book[0]

    print("Creating review...")
    cursor.execute("""
        SELECT 1 FROM PersonalRating WHERE isbn = %s""", (isbn,))

    if cursor.fetchone():
        # UPDATE PersonalRating
        # SET
        # rating = 5,
        # text_review = 'This is my new favorite'
        # WHERE ISBN = '9781984854032';
        print("Updating Book Review\n")

        cursor.execute("""
            UPDATE PersonalRating
            SET
                    rating = %s,
                    text_review = %s
            WHERE ISBN = %s
            """, (rating, review, isbn))

        conn.commit()
        print("Book review successfully updated")
        return

    # INSERT INTO PersonalRating (ISBN, rating, text_review)
    # VALUES ('9781984854032', 5,
    # 'Inspirational and practical for leaders!')
    cursor.execute("""
        INSERT INTO PersonalRating (isbn, rating, text_review)
        VALUES (%s, %s, %s)
        """, (isbn, rating, review))

    conn.commit()
    print("Book review created!")


# f
def remove_from_shelf(): # DELETE FROM AddedToShelf
    book_name = input("Enter book name: ")
    author_name = input("Enter author name: ")
    shelf_name = input("Enter shelf name: ")

# g
def show_by_rating():
    # SELECT b.title, b.ISBN, p.rating
    # FROM Book b
    # JOIN PersonalRating p ON b.ISBN = p.ISBN
    # ORDER BY p.rating DESC, b.title ASC;
    cursor.execute("""
        SELECT b.title, b.isbn, p.rating
        FROM Book b
        JOIN PersonalRating p ON b.isbn = p.isbn 
        ORDER BY p.rating DESC, b.title ASC;
        """)

    results = cursor.fetchall()
    if not results:
        print("No ratings found.")
        return

    print("\nBooks Sorted by Rating\n")
    print(f"{'Title':65} | {'ISBN':15} | Rating")
    print("-" * 81)

    for title, isbn, rating in results:
        print(f"{title[:65]:65} | {isbn:15} | {rating}")

# h
def show_by_author():
    # SELECT b.title, b.ISBN
    # FROM Book b
    # JOIN Writes w ON b.ISBN = w.ISBN
    # JOIN Author a ON w.author_id = a.author_id
    # WHERE a.name = 'Josh Kaufman';
    author_name = input("Enter author name: ")

    cursor.execute("""
        SELECT b.title, b.isbn
        FROM Book b
        JOIN Writes w ON b.isbn = w.isbn
        JOIN Author a ON w.author_id = a.author_id
        WHERE a.name = %s
        """, (author_name,))

    results = cursor.fetchall()
    if not results:
        print("Author not found")
        return

    print("\nBooks Sorted by Author\n")
    print(f"{'Title':65} | {'ISBN':15}")
    print("-" * 80)

    for title, isbn in results:
        print(f"{title[:65]:65} | {isbn:15}")
    return
# i
def show_currently_reading():
    # SELECT b.title, b.ISBN, bs.progress_page
    # FROM Book b
    # JOIN BookStatus bs ON b.ISBN = bs.ISBN
    # WHERE bs.read_status = 'CURRENTLY_READING';
    return

# j
def show_want_to_read():
    # SELECT b.title, b.ISBN
    # FROM Book b
    # JOIN BookStatus bs ON b.ISBN = bs.ISBN
    # WHERE bs.read_status = 'WANT_TO_READ';
    return

# k
def show_bookshelf_most():
    # SELECT ds.name AS shelf_name, COUNT(ats.ISBN) AS book_count
    # FROM DigitalShelf ds
    # JOIN AddedToShelf ats ON ds.shelf_id = ats.shelf_id
    # GROUP BY ds.shelf_id, ds.name
    # ORDER BY book_count DESC;
    return



if __name__ == "__main__":
    main()
