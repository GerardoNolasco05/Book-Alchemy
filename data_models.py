from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String)
    author_birth_date = Column(Integer)
    author_date_of_death = Column(Integer)

    # Relationship to link books to this author
    books = relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"Author(author_id={self.author_id}, name={self.author_name})"


class Book(db.Model):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(Integer)
    book_title = Column(String)
    book_publication_year = Column(Integer)

    # Foreign Key linking the book to an author
    author_id = Column(Integer, ForeignKey('authors.author_id'), nullable=False)

    def __repr__(self):
        return f"Book(book_id={self.book_id}, title={self.book_title}, author_id={self.author_id})"
