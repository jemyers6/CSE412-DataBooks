import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    try:
        conn = sqlite3.connect('my_books.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS books 
                        (isbn TEXT PRIMARY KEY,
                         title TEXT, 
                         author TEXT, 
                         genre TEXT, 
                         editor TEXT,
                         publication_year INT, 
                         edition TEXT,
                         list_price_usd REAL,
                         rating REAL, 
                         citation TEXT,
                         language TEXT,  -- Added language field
                         printing_location TEXT,
                         number_of_pages INT)''')  # Added printing_location field
        conn.execute('''CREATE TABLE IF NOT EXISTS genres
                        (genre_id INTEGER PRIMARY KEY, 
                         genre_name TEXT UNIQUE)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS authors
                        (author_id INTEGER PRIMARY KEY, 
                         author_name TEXT UNIQUE)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS book_genre
                        (isbn TEXT, genre_id INTEGER,
                         FOREIGN KEY (isbn) REFERENCES books(isbn),
                         FOREIGN KEY (genre_id) REFERENCES genres(genre_id))''')
        conn.execute('''CREATE TABLE IF NOT EXISTS book_author
                        (isbn TEXT, author_id INTEGER,
                         FOREIGN KEY (isbn) REFERENCES books(isbn),
                         FOREIGN KEY (author_id) REFERENCES authors(author_id))''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            conn.close()

def format_author_name(author):
    parts = author.split()
    if len(parts) > 1:
        last_name = parts[-1]
        initials = ''.join([name[0] for name in parts[:-1]])
        formatted_author = f"{last_name}, {initials}."
    else:
        formatted_author = author
    return formatted_author

def generate_apa_citation(author, publication_year, title, edition, editor):
    formatted_author = format_author_name(author)
    title_parts = title.split(':')
    formatted_title_parts = [part.capitalize() for part in title_parts]
    formatted_title = ': '.join(formatted_title_parts)
    if edition.lower() == "first":
        citation = f"{formatted_author} ({publication_year}). {formatted_title}. {editor}."
    else:
        citation = f"{formatted_author} ({publication_year}). {formatted_title}. ({edition} ed.). {editor}."
    return citation

def add_book():
    conn = None
    try:
        conn = sqlite3.connect('my_books.db')
        cursor = conn.cursor()

        citation = generate_apa_citation(author_entry.get(), publication_year_entry.get(), title_entry.get(), edition_entry.get(), editor_entry.get())

        cursor.execute("INSERT INTO books (isbn, title, author, genre, editor, publication_year, edition, list_price_usd, rating, citation, language, printing_location, number_of_pages) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (isbn_entry.get(), title_entry.get(), author_entry.get(), genre_entry.get(), editor_entry.get(), publication_year_entry.get(), edition_entry.get(), list_price_usd_entry.get(), rating_entry.get(), citation, language_entry.get(), printing_location_entry.get(), number_of_pages_entry.get()))

        genres = [g.strip() for g in genre_entry.get().split(',')]
        for genre in genres:
            cursor.execute("INSERT OR IGNORE INTO genres (genre_name) VALUES (?)", (genre,))
            cursor.execute("SELECT genre_id FROM genres WHERE genre_name = ?", (genre,))
            genre_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO book_genre (isbn, genre_id) VALUES (?, ?)", (isbn_entry.get(), genre_id))

        authors = [a.strip() for a in author_entry.get().split(',')]
        for author in authors:
            cursor.execute("INSERT OR IGNORE INTO authors (author_name) VALUES (?)", (author,))
            cursor.execute("SELECT author_id FROM authors WHERE author_name = ?", (author,))
            author_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO book_author (isbn, author_id) VALUES (?, ?)", (isbn_entry.get(), author_id))
        
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            conn.close()
    clear_entries()

def search_books():
    conn = None
    try:
        conn = sqlite3.connect('my_books.db')
        search_query = search_entry.get()
        search_type = search_type_var.get()
        
        if search_type == "Title":
            query = "SELECT * FROM books WHERE title LIKE ?"
        elif search_type == "Author":
            query = "SELECT * FROM books WHERE author LIKE ?"
        elif search_type == "Genre":
            query = "SELECT * FROM books WHERE genre LIKE ?"
        elif search_type == "Editor":
            query = "SELECT * FROM books WHERE editor LIKE ?"
        elif search_type == "Publication Year":
            query = "SELECT * FROM books WHERE publication_year LIKE ?"
        elif search_type == "Edition":
            query = "SELECT * FROM books WHERE edition LIKE ?"
        else:
            query = "SELECT * FROM books WHERE title LIKE ?"
        
        cursor = conn.execute(query, ('%' + search_query + '%',))
        records = cursor.fetchall()
        listbox.delete(0, tk.END)
        for record in records:
            listbox.insert(tk.END, record)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            conn.close()

def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    editor_entry.delete(0, tk.END)
    publication_year_entry.delete(0, tk.END)
    edition_entry.delete(0, tk.END)
    list_price_usd_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)
    language_entry.delete(0, tk.END)  # Clear language entry
    printing_location_entry.delete(0, tk.END)  # Clear printing_location entry
    number_of_pages_entry.delete(0, tk.END) # Add this line to clear number_of_pages entry

create_db()

root = tk.Tk()
root.title("Book Library")

frame = tk.Frame(root)
frame.pack(pady=10)

# Fields for book information
title_label = tk.Label(frame, text="Title")
title_label.grid(row=0, column=0)
title_entry = tk.Entry(frame)
title_entry.grid(row=0, column=1)

author_label = tk.Label(frame, text="Author(s)")
author_label.grid(row=1, column=0)
author_entry = tk.Entry(frame)
author_entry.grid(row=1, column=1)

genre_label = tk.Label(frame, text="Genre(s)")
genre_label.grid(row=2, column=0)
genre_entry = tk.Entry(frame)
genre_entry.grid(row=2, column=1)

editor_label = tk.Label(frame, text="Editor")
editor_label.grid(row=3, column=0)
editor_entry = tk.Entry(frame)
editor_entry.grid(row=3, column=1)

publication_year_label = tk.Label(frame, text="Publication Year")
publication_year_label.grid(row=4, column=0)
publication_year_entry = tk.Entry(frame)
publication_year_entry.grid(row=4, column=1)

edition_label = tk.Label(frame, text="Edition")
edition_label.grid(row=5, column=0)
edition_entry = tk.Entry(frame)
edition_entry.grid(row=5, column=1)

list_price_usd_label = tk.Label(frame, text="List Price USD $")
list_price_usd_label.grid(row=6, column=0)
list_price_usd_entry = tk.Entry(frame)
list_price_usd_entry.grid(row=6, column=1)

isbn_label = tk.Label(frame, text="ISBN")
isbn_label.grid(row=7, column=0)
isbn_entry = tk.Entry(frame)
isbn_entry.grid(row=7, column=1)

rating_label = tk.Label(frame, text="Rating")
rating_label.grid(row=8, column=0)
rating_entry = tk.Entry(frame)
rating_entry.grid(row=8, column=1)

language_label = tk.Label(frame, text="Language")  # Added Language label
language_label.grid(row=9, column=0)  # Added Language row
language_entry = tk.Entry(frame)  # Added Language entry
language_entry.grid(row=9, column=1)  # Added Language column

printing_location_label = tk.Label(frame, text="Printing Location")  # Added Printing Location label
printing_location_label.grid(row=10, column=0)  # Added Printing Location row
printing_location_entry = tk.Entry(frame)  # Added Printing Location entry
printing_location_entry.grid(row=10, column=1)  # Added Printing Location column

number_of_pages_label = tk.Label(frame, text="Number of Pages")
number_of_pages_label.grid(row=11, column=0)
number_of_pages_entry = tk.Entry(frame)
number_of_pages_entry.grid(row=11, column=1)

add_button = tk.Button(frame, text="Add Book", command=add_book)
add_button.grid(row=12, column=0, columnspan=3)

# Search functionality
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Search")
search_label.pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT)

search_type_var = tk.StringVar()
search_type_var.set("Title")
search_type_menu = tk.OptionMenu(search_frame, search_type_var, "Title", "Author", "Genre", "Editor", "Publication Year", "Edition")
search_type_menu.pack(side=tk.LEFT)

search_button = tk.Button(search_frame, text="Search", command=search_books)
search_button.pack(side=tk.LEFT)

listbox = tk.Listbox(root, width=100)
listbox.pack(pady=20)

root.mainloop()