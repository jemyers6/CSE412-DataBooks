import psycopg2
import datetime

# may need to change this based on your local database name
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="booksdb"
)

cursor = conn.cursor()

def main():
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
    book_name = input("Enter book name: ")  # could take ISBN, but that does make it less user-friendly
    author_name = input("Enter author name: ")

# b
def create_shelf(): # INSERT INTO DigitalShelf (shelf_id, name, shelf_type)
    shelf_name = input("Enter name of new shelf: ")
    shelf_type = input("Enter type of new shelf: ")
    # get shelf id as the next num in number of shelves

# c
def update_status(): # UPDATE BookStatus
    book_name = input("Enter book name: ")
    author_name = input("Enter author name: ")
    progress_page = input("Enter current page: ")
    new_status = input("Enter updated status: ")
    current_time = datetime.datetime.now()

# d
def delete_bookshelf(): # DELETE FROM DigitalShelf
    shelf_name = input("Enter bookshelf Name: ")

# e
def create_review(): # INSERT INTO PersonalRating (ISBN, rating, text_review)
    book_name = input("Enter book name: ")
    author_name = input("Enter author name: ")
    rating = input("Enter rating from 1-5: ")
    review = input("Enter review: ")

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
    return

# h
def show_by_author():
    # SELECT b.title, b.ISBN
    # FROM Book b
    # JOIN Writes w ON b.ISBN = w.ISBN
    # JOIN Author a ON w.author_id = a.author_id
    # WHERE a.name = 'Josh Kaufman';
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
