import psycopg2
import datetime
from datetime import date
import os

# fallback
DB_USER = os.getenv("DB_USER", "postgres")       
DB_NAME = os.getenv("DB_NAME", "databooks")
DB_PORT = os.getenv("DB_PORT", "8888")

conn = psycopg2.connect(
    host="localhost",
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER
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
        print("i. Show read")
        print("j. Show currently reading")
        print("k. Show want to read")
        print("l. Show bookshelf with the most amount of books")
        print("m. View all books")
        print("n. Show shelves with their books")
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
            show_books_read()
            
        elif choice == 'j':
            show_currently_reading()

        elif choice == 'k':
            show_want_to_read()

        elif choice == 'l':
            show_bookshelf_most()

        elif choice == 'm':
            show_all_books()

        elif choice == 'n':
            show_shelves_with_books()

        elif choice == 'q':
            print("Thank you for using DataBooks!")
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Try again.")

# a
def add_to_shelf(): # INSERT INTO AddedToShelf (shelf_id, ISBN)
    
    shelf_selection = select_shelf_by_number()
    if shelf_selection is None:
        return

    shelf_id, shelf_name, shelf_type = shelf_selection

    book_selection = select_book_by_number()
    if book_selection is None:
        return

    isbn, title, authors = book_selection

    cursor.execute("""
        SELECT 1 FROM AddedToShelf
        WHERE shelf_id = %s AND isbn = %s
        """, (shelf_id, isbn))

    if cursor.fetchone():
        print(f"'{title}' is already in shelf '{shelf_name}'.")
        return

    cursor.execute("""
        INSERT INTO AddedToShelf (shelf_id, isbn)
        VALUES (%s, %s)
        """, (shelf_id, isbn))

    cursor.execute("SELECT 1 FROM BookStatus WHERE isbn = %s", (isbn,))
    if not cursor.fetchone():
        today = date.today().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO BookStatus (isbn, progress_page, read_status, updated_at, start_date, finish_date)
            VALUES (%s, %s, %s, %s, %s, NULL)
        """, (isbn, 0, 'WANT_TO_READ', today, today))

    cursor.execute("SELECT 1 FROM PersonalRating WHERE isbn = %s", (isbn,))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO PersonalRating (isbn, rating, text_review)
            VALUES (%s, %s, %s)
        """, (isbn, None, 'Not rated yet'))

    conn.commit()

    print("Book successfully added to shelf!")

# b
def create_shelf(): # INSERT INTO DigitalShelf (shelf_id, name, shelf_type)
    # INSERT INTO DigitalShelf (shelf_id, name, shelf_type)
    #   VALUES (11, 'Dark Academia','OTHER');
    shelf_name = input("Enter name of new shelf: ")
    shelf_type = "OTHER"
    
    cursor.execute("""
        SELECT shelf_id
        FROM DigitalShelf
        WHERE name = %s
        """, (shelf_name,))

    shelf = cursor.fetchone()
    if shelf:
        print("Shelf already exists!")
        return

    cursor.execute("SELECT COALESCE(MAX(shelf_id), 0) + 1 FROM DigitalShelf;")
    next_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO DigitalShelf (shelf_id, name, shelf_type)
                   VALUES (%s, %s, %s)
                   """, (next_id, shelf_name, shelf_type))

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

    shelf_selection = select_shelf_by_number()
    if shelf_selection is None:
        return
    shelf_id, shelf_name, shelf_type = shelf_selection

    book_selection = select_book_on_shelf_by_number(shelf_id)
    if book_selection is None:
        return
    isbn, title, authors = book_selection

    new_status = select_read_status()
    if new_status is None:
        return

    if new_status == "READ":
        cursor.execute("SELECT num_pages FROM Book WHERE isbn = %s", (isbn,))
        row = cursor.fetchone()
        progress_page = row[0]
    else:
        while True:
            progress_input = input("Enter current page: ").strip()
            if not progress_input.isdigit():
                print("Please enter a non-negative number for the page.")
                continue
            progress_page = int(progress_input)
            if progress_page < 0:
                print("Page cannot be negative")
                continue
            break

    today = date.today()
    cur_date = today.strftime("%Y-%m-%d")


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

    print(f"Book {title} status successfully to {new_status}")


# d
def delete_bookshelf(): # DELETE FROM DigitalShelf
    # DELETE FROM DigitalShelf
    # WHERE shelf_id = 1;
    shelf_selection = select_shelf_by_number()
    if shelf_selection is None:
        return

    shelf_id, shelf_name, shelf_type = shelf_selection

    print("Deleting bookshelf...")
    cursor.execute("""
        DELETE FROM DigitalShelf
        WHERE shelf_id = %s
        """, (shelf_id,))

    conn.commit()

    print("Bookshelf successfully deleted")

# e
def create_review(): # INSERT INTO PersonalRating (ISBN, rating, text_review)

    shelf_selection = select_shelf_by_number()
    if shelf_selection is None:
        return
    shelf_id, shelf_name, shelf_type = shelf_selection

    book_selection = select_book_on_shelf_by_number(shelf_id)
    if book_selection is None:
        return
    isbn, title, authors = book_selection

    rating = input("Enter rating of 1, 2, 3, 4, or 5: ")
    review = input("Enter review: ")

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
    # DELETE FROM AddedToShelf
    # WHERE shelf_id = 1 AND ISBN = '9781984854032';

    shelf_selection = select_shelf_by_number()
    if shelf_selection is None:
        return

    shelf_id, shelf_name, shelf_type = shelf_selection

    book_selection = select_book_on_shelf_by_number(shelf_id)
    if book_selection is None:
        return
    isbn, title, authors = book_selection

    isbn, title, authors = book_selection

    cursor.execute("""
        SELECT 1 FROM AddedToShelf
        WHERE shelf_id = %s AND isbn = %s
        """, (shelf_id, isbn))

    if cursor.fetchone():
        print("Removing book from shelf...")
        cursor.execute("""
            DELETE FROM AddedToShelf
            WHERE shelf_id = %s AND isbn = %s
            """, (shelf_id, isbn))
        conn.commit()
        print("Book successfully deleted from shelf.")
        return
    else:
        print("Book is not in shelf.")

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
    author_selection = select_author_by_number()
    if author_selection is None:
        return

    author_id, author_name = author_selection

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

#i
def show_books_read():
    # SELECT b.title, b.ISBN, bs.progress_page
    # FROM Book b
    # JOIN BookStatus bs ON b.ISBN = bs.ISBN
    # WHERE bs.read_status = 'READ';
    cursor.execute("""
        SELECT b.title, b.isbn, bs.progress_page
        FROM Book b
        JOIN BookStatus bs ON b.isbn = bs.isbn
        WHERE bs.read_status = 'READ';""")

    results = cursor.fetchall()
    if not results:
        print("Not currently reading any books.")
        return

    print("\nBooks Read\n")
    print(f"{'Title':65} | {'ISBN':15} | {'Progress Page':3}")
    print("-" * 85)

    for title, isbn, progress_page in results:
        print(f"{title[:65]:65} | {isbn:15} | {progress_page:3}")

def show_currently_reading():
    # SELECT b.title, b.ISBN, bs.progress_page
    # FROM Book b
    # JOIN BookStatus bs ON b.ISBN = bs.ISBN
    # WHERE bs.read_status = 'CURRENTLY_READING';
    cursor.execute("""
        SELECT b.title, b.isbn, bs.progress_page
        FROM Book b
        JOIN BookStatus bs ON b.isbn = bs.isbn
        WHERE bs.read_status = 'CURRENTLY_READING';""")

    results = cursor.fetchall()
    if not results:
        print("Not currently reading any books.")
        return

    print("\nBooks currently reading\n")
    print(f"{'Title':65} | {'ISBN':15} | {'Progress Page':3}")
    print("-" * 85)

    for title, isbn, progress_page in results:
        print(f"{title[:65]:65} | {isbn:15} | {progress_page:3}")

# j
def show_want_to_read():
    # SELECT b.title, b.ISBN
    # FROM Book b
    # JOIN BookStatus bs ON b.ISBN = bs.ISBN
    # WHERE bs.read_status = 'WANT_TO_READ';
    cursor.execute("""
        SELECT b.title, b.isbn
        FROM Book b
        JOIN BookStatus bs ON b.isbn = bs.isbn
        WHERE bs.read_status = 'WANT_TO_READ';""")

    results = cursor.fetchall()
    if not results:
        print("No books are currently marked as \"Want to Read\"")
        return

    print("\nBooks \"Want To Read\"\n")
    print(f"{'Title':65} | {'ISBN':15}")
    print("-" * 80)

    for title, isbn in results:
        print(f"{title[:65]:65} | {isbn:15}")

# k
def show_bookshelf_most():
    # SELECT ds.name AS shelf_name, COUNT(ats.ISBN) AS book_count
    # FROM DigitalShelf ds
    # JOIN AddedToShelf ats ON ds.shelf_id = ats.shelf_id
    # GROUP BY ds.shelf_id, ds.name
    # ORDER BY book_count DESC;
    cursor.execute("""
        SELECT ds.name AS shelf_name, COUNT(ats.ISBN) AS book_count
        FROM DigitalShelf ds
        JOIN AddedToShelf ats ON ds.shelf_id = ats.shelf_id
        GROUP BY ds.shelf_id, ds.name
        ORDER BY book_count DESC;""")

    results = cursor.fetchall()
    if not results:
        print("No bookshelf found.")
        return

    ds_name = results[0][0]
    count = results[0][1]

    print("\nBookshelf with the most books\n")
    print(f"Bookshelf: {ds_name}")
    print(f"Number of Books: {count}")

def show_all_books():

    cursor.execute("""
        SELECT b.isbn,
               b.title,
               COALESCE(string_agg(a.name, ', ' ORDER BY a.name), 'Unknown') AS authors
        FROM Book b
        LEFT JOIN Writes w ON b.isbn = w.isbn
        LEFT JOIN Author a ON w.author_id = a.author_id
        GROUP BY b.isbn, b.title
        ORDER BY b.title;""")

    rows = cursor.fetchall()

    if not rows:
        print("No books found in the database.")
        return

    print("\nAll Books\n")
    print(f"{'Title':65} | {'Authors':35} | {'ISBN':15}")
    print("-" * 120)

    for isbn, title, authors in rows:
        print(f"{title[:65]:65} | {authors[:35]:35} | {isbn:15}")

def show_shelves_with_books():

    cursor.execute("""
        SELECT 
            ds.shelf_id,
            ds.name AS shelf_name,
            ds.shelf_type,
            b.title,
            COALESCE(string_agg(a.name, ', ' ORDER BY a.name), 'Unknown') AS authors,
            b.isbn,
            bs.read_status,
            bs.progress_page,
            bs.updated_at,
            bs.start_date,
            bs.finish_date,
            pr.rating,
            pr.text_review
        FROM DigitalShelf ds
        LEFT JOIN AddedToShelf ats ON ds.shelf_id = ats.shelf_id
        LEFT JOIN Book b ON ats.isbn = b.isbn
        LEFT JOIN Writes w ON b.isbn = w.isbn
        LEFT JOIN Author a ON w.author_id = a.author_id
        LEFT JOIN BookStatus bs ON b.isbn = bs.isbn
        LEFT JOIN PersonalRating pr ON b.isbn = pr.isbn
        GROUP BY 
            ds.shelf_id, ds.name, ds.shelf_type, 
            b.title, b.isbn,
            bs.read_status, bs.progress_page, bs.updated_at, bs.start_date, bs.finish_date,
            pr.rating, pr.text_review
        ORDER BY ds.shelf_id, b.title;
    """)

    rows = cursor.fetchall()

    if not rows:
        print("No shelves or shelved books found.")
        return

    current_shelf = None

    for (shelf_id, shelf_name, shelf_type,
        title, authors, isbn,status, progress, 
        updated_at, start_date, finish_date,
        rating, text_review) in rows:

        if current_shelf != shelf_id:
            current_shelf = shelf_id
            print("-" * 110)
            print(f"Shelf {shelf_name} ")

        if title is None:
            print("  (No books on this shelf)")
        else:
            status_display = status if status else "NO STATUS"
            progress_display = progress if progress is not None else "-"
            updated_display = updated_at if updated_at else "-"
            start_display = start_date if start_date else "-"
            finish_display = finish_date if finish_date else "-"
            rating_display = rating if rating is not None else "Not rated"
            review_display = text_review if text_review else ""

            print(
                f"  - {title} — {authors} (ISBN: {isbn})\n"
                f"      Status: {status_display}, Page: {progress_display}, "
                f"Updated: {updated_display}, Start: {start_display}, Finish: {finish_display}\n"
                f"      Rating: {rating_display}, Review: {review_display}")

    print("-" * 110)

def select_book_by_number():

    cursor.execute("""
        SELECT b.isbn,
               b.title,
               COALESCE(string_agg(a.name, ', ' ORDER BY a.name), 'Unknown') AS authors
        FROM Book b
        LEFT JOIN Writes w ON b.isbn = w.isbn
        LEFT JOIN Author a ON w.author_id = a.author_id
        GROUP BY b.isbn, b.title
        ORDER BY b.title;
    """)
    rows = cursor.fetchall()

    if not rows:
        print("No books found in the database.")
        return None

    print("\nAvailable Books:\n")
    for idx, (isbn, title, authors) in enumerate(rows, start=1):
        print(f"{idx}. {title} — {authors} (ISBN: {isbn})")

    while True:
        choice = input("\nEnter the number of the book you want to select or q to cancel: ").strip().lower()
        if choice == 'q':
            print("Cancelled book selection.")
            return None

        if not choice.isdigit():
            print("Please enter a valid number or q to cancel.")
            continue

        choice_num = int(choice)
        if 1 <= choice_num <= len(rows):
            isbn, title, authors = rows[choice_num - 1]
            return isbn, title, authors
        else:
            print(f"Please enter a number between 1 and {len(rows)}.")

def select_shelf_by_number():
    cursor.execute("""
        SELECT shelf_id, name, shelf_type
        FROM DigitalShelf
        ORDER BY shelf_id;
    """)
    rows = cursor.fetchall()

    if not rows:
        print("No bookshelves found. Create a shelf first (option b).")
        return None

    print("\nAvailable Bookshelves:\n")
    for idx, (shelf_id, name, shelf_type) in enumerate(rows, start=1):
        print(f"{idx}. {name}")

    while True:
        choice = input("\nEnter the number of the shelf you want to use or q to cancel): ").strip().lower()
        if choice == 'q':
            print("Cancelled shelf selection.")
            return None

        if not choice.isdigit():
            print("Please enter a valid number or q to cancel.")
            continue

        choice_num = int(choice)
        if 1 <= choice_num <= len(rows):
            shelf_id, name, shelf_type = rows[choice_num - 1]
            return shelf_id, name, shelf_type
        else:
            print(f"Please enter a number between 1 and {len(rows)}.")

def select_book_on_shelf_by_number(shelf_id):
    # shows the books that are shelved by user
    cursor.execute("""
        SELECT b.isbn,
               b.title,
               COALESCE(string_agg(a.name, ', ' ORDER BY a.name), 'Unknown') AS authors
        FROM AddedToShelf ats
        JOIN Book b ON ats.isbn = b.isbn
        LEFT JOIN Writes w ON b.isbn = w.isbn
        LEFT JOIN Author a ON w.author_id = a.author_id
        WHERE ats.shelf_id = %s
        GROUP BY b.isbn, b.title
        ORDER BY b.title;
    """, (shelf_id,))
    rows = cursor.fetchall()

    if not rows:
        print("No books found on this shelf.")
        return None

    print("\nBooks on this shelf:\n")
    for idx, (isbn, title, authors) in enumerate(rows, start=1):
        print(f"{idx}. {title} — {authors} (ISBN: {isbn})")

    while True:
        choice = input("\nEnter the number of the book you want to select or q to cancel: ").strip().lower()
        if choice == 'q':
            print("Cancelled book selection.")
            return None

        if not choice.isdigit():
            print("Please enter a valid number or q to cancel.")
            continue

        choice_num = int(choice)
        if 1 <= choice_num <= len(rows):
            isbn, title, authors = rows[choice_num - 1]
            return isbn, title, authors
        else:
            print(f"Please enter a number between 1 and {len(rows)}.")

def select_read_status():

    options = [ "WANT_TO_READ", "CURRENTLY_READING", "READ"]
    print("\nSelect book status:")

    for idx, status in enumerate(options, start=1):
        print(f"{idx}. {status}")
    print("q. Cancel")

    while True:
        choice = input("Enter choice: ").strip().lower()
        if choice == "q":
            print("Cancelled status selection.")
            return None

        if not choice.isdigit():
            print("Please enter 1, 2, 3, or q to cancel.")
            continue

        idx = int(choice)
        if 1 <= idx <= len(options):
            status_value = options[idx - 1]
            return status_value

        else:
            print(f"Please enter a number between 1 and {len(options)}, or q to cancel.")

def select_author_by_number():

    cursor.execute("""
        SELECT author_id, name
        FROM Author
        ORDER BY name;""")
    
    rows = cursor.fetchall()

    if not rows:
        print("No authors found in the database.")
        return None

    print("\nAvailable Authors:\n")
    for idx, (author_id, name) in enumerate(rows, start=1):
        print(f"{idx:3}. {name}")

    while True:
        choice = input("\nEnter the number of the author you want to select or q to cancel): ").strip().lower()
        if choice == 'q':
            print("Cancelled author selection.")
            return None

        if not choice.isdigit():
            print("Please enter a valid number or q to cancel.")
            continue

        idx = int(choice)
        if 1 <= idx <= len(rows):
            return rows[idx - 1]  
        else:
            print(f"Please enter a number between 1 and {len(rows)}.")

if __name__ == "__main__":
    main()
