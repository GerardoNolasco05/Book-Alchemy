from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/gerardonolasco/Documents/Software_Engineer/Codio/book_app/Book-Alchemy/data/library.sqlite'
app.config['SECRET_KEY'] = 'your_secret_key_here'  # For flash messages
db.init_app(app)

@app.route('/')
def home():
    sort_by = request.args.get('sort_by', 'title')  # Default sort by title
    search_query = request.args.get('search', '').strip()  # Get search input

    # Start with a base query that includes Book and Author
    query = Book.query.join(Author)

    # Filter books if there is a search query
    if search_query:
        search_results = query.filter(
            (Book.book_title.ilike(f"%{search_query}%")) |
            (Author.author_name.ilike(f"%{search_query}%"))
        ).all()  # Books that match search

        # Exclude search results from the general query
        remaining_books = query.filter(~((Book.book_title.ilike(f"%{search_query}%")) |
                                         (Author.author_name.ilike(f"%{search_query}%"))))
    else:
        search_results = []
        remaining_books = query

    # Apply sorting to the remaining books
    if sort_by == "author":
        remaining_books = remaining_books.order_by(Author.author_name.asc()).all()
    else:
        remaining_books = remaining_books.order_by(Book.book_title.asc()).all()

    # Combine search results (at the top) with the remaining sorted books
    books = search_results + remaining_books

    return render_template('home.html', books=books, sort_by=sort_by, search_query=search_query)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Getting the form data
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')  # Selected author

        # Create a new Book instance
        new_book = Book(book_isbn=isbn, book_title=title, book_publication_year=publication_year, author_id=author_id)

        # Add the book to the database
        try:
            db.session.add(new_book)
            db.session.commit()
            flash('Book successfully added!', 'success')  # Flash success message for book
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')  # Flash error message for any issue

        return redirect(url_for('add_book'))

    # For GET request, render the form
    authors = Author.query.all()  # Get all authors from the database
    return render_template('add_book.html', authors=authors)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        # Getting the form data
        name = request.form.get('name')
        birthdate = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')

        # Create a new Author instance
        new_author = Author(author_name=name, author_birth_date=birthdate, author_date_of_death=date_of_death)

        # Add the author to the database
        try:
            db.session.add(new_author)
            db.session.commit()
            flash('Author successfully added!', 'success')  # Flash success message for author
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')  # Flash error message for any issue

        return redirect(url_for('add_author'))

    # For GET request, render the form
    return render_template('add_author.html')

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    # Fetch the book using the correct primary key field (book_id)
    book = Book.query.get_or_404(book_id)

    try:
        # Remove the book from the database
        db.session.delete(book)
        db.session.commit()
        flash(f'Book "{book.book_title}" successfully deleted!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')

    # After deletion, redirect to the home page
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
