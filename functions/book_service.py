import mysql.connector
from functions.books import book_json_response
from functions.data_class import Book, Db_config

class Book_service():
    def __init__(self, db_config: Db_config):
        self.connector = mysql.connector.connect(**db_config)
        self.cursor = self.connector.cursor(dictionary=True)
    def close_connection(self) -> None:
        self.cursor.close()
        self.connector.close()

    def get_books(self) -> list[Book]:
        self.cursor.execute(
            'SELECT * FROM books',
        )
        rows = self.cursor.fetchall()
        self.connector.commit()
        self.close_connection()
        return book_json_response(rows)
    
    def delete_book(self, book_id: int) -> str:
        self.cursor.execute(
            'SELECT * FROM books WHERE book_id =%s',
            (book_id,)
        )
        rows = self.cursor.fetchall()
        if rows == []:
            self.connector.commit()
            self.close_connection()
            return f"No book with book id {book_id} found "
        else:
            self.cursor.execute(
                'DELETE FROM books WHERE book_id = %s',
                (book_id,)
            )
            self.connector.commit()
            self.close_connection()
            return f"Deleted successfully"
    
    def post_book(self, data) -> list[Book]:
        self.cursor.execute(
            'INSERT INTO books(title, date_of_writing, author) VALUES(%s,%s,%s)',
            (data.get('name'), data.get('dateOfWriting'), data.get('author'))
        )
        self.cursor.execute(
            'SELECT * FROM books WHERE title = %s AND date_of_writing = %s AND author = %s ORDER BY book_id DESC LIMIT 1',
            (data.get('name'), data.get('dateOfWriting'), data.get('author'))
        )
        rows = self.cursor.fetchall()
        self.connector.commit()
        self.close_connection()
        return book_json_response(rows)

    def put_book(self, data) -> list[Book]:
        self.cursor.execute(
            'UPDATE books SET title = %s, date_of_writing = %s, author = %s WHERE book_id = %s',
            (data.get('name'), data.get('dateOfWriting'), data.get('author'), data.get('id'))
        )
        self.cursor.execute(
            'SELECT * FROM books WHERE book_id = %s',
            (data.get('id'), )
        )
        rows = self.cursor.fetchall()

        self.connector.commit()
        self.close_connection()
        return book_json_response(rows)