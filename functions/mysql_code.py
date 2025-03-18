import mysql.connector
from functions.data_class import Db_config
from functions.data_class import Book_from_db, Book, Author, Book_id_Author_id, Book_to_upload


class Mysql_code():
    def __init__(self, db_config: Db_config) -> None:
        self.connector = mysql.connector.connect(**db_config)
        self.cursor = self.connector.cursor(dictionary=True)

    def close_connection(self) -> None:
        self.cursor.close()
        self.connector.close()

    def commit_close(self) -> None:
        self.connector.commit()
        self.close_connection()

    def select_all_books_and_author(self) -> list[Book_from_db]:
        self.cursor.execute(
        """
        SELECT books2.book_id,
               books2.title,
               books2.year_of_publish,
               authors.full_name AS author,
               books2.pages,
               books2.image_base64,
               books2.description
        FROM book_id_author_id
        INNER JOIN books2 ON
        book_id_author_id.book_id = books2.book_id
        INNER JOIN authors ON
        book_id_author_id.author_id = authors.author_id
        """
        )
        rows = self.cursor.fetchall()
        self.commit_close()
        return rows
    
    def select_all_authors(self) -> list[Author]:
        self.cursor.execute(
            """
                SELECT * FROM authors
            """
        )
        rows = self.cursor.fetchall()
        self.commit_close()
        return rows

    def delete_from_books(self, book_id:int) -> None:
        self.cursor.execute(
            """
                DELETE FROM books2 WHERE book_id = %s
            """,
            (book_id,)
        )
        self.commit_close()

    def delete_from_book_id_author_id(self, book_id:int) -> None:
        self.cursor.execute(
            """
                DELETE FROM book_id_author_id WHERE book_id = %s
            """,
            (book_id,)
        )
        self.connector.commit()

    def delete_from_authors(self, author_id:int) -> None:
        rows = self.check_for_author_in_book_id_author_id(author_id)
        if not rows:
            self.cursor.execute(
            """
                DELETE FROM authors WHERE author_id = %s
            """,
            (author_id,)
        )
            self.delete_from_book_id_author_id(author_id)
        self.commit_close()

    def check_for_author_in_book_id_author_id(self, author_id:int) -> Book_id_Author_id:
        self.cursor.execute(
            """
                SELECT * FROM book_id_author_id WHERE author_id = %s
            """,
            (author_id,)
        )
        rows = self.cursor.fetchall()
        self.commit_close()
        return rows

    def get_book_by_name(self, book_name:str) -> list[Book]:

        search_pattern = f"%{book_name}%"

        self.cursor.execute(
            """
                SELECT books2.book_id,
                       books2.title,
                       books2.year_of_publish,
                       authors.full_name AS author,
                       books2.pages,
                       books2.image_base64,
                       books2.description
                FROM book_id_author_id
                INNER JOIN books2 ON
                    book_id_author_id.book_id = books2.book_id
                INNER JOIN authors ON
                    book_id_author_id.author_id = authors.author_id
                WHERE title LIKE %s OR authors.full_name LIKE %s
            """,
            (search_pattern, search_pattern)
        )
        rows = self.cursor.fetchall()
        self.commit_close()
        return rows
    
    def insert_new_author(self, data:Book_to_upload) -> None:
        self.cursor.execute(
                """
                    INSERT INTO authors(full_name) 
                    VALUES(%s)
                """,
                (data.get('author'),)
            )
        self.connector.commit()

    def insert_book_into_books(self, data:Book_to_upload) -> None:
        self.cursor.execute(
            """
                INSERT INTO books2(title, year_of_publish, pages, description, image_base64) 
                VALUES (%s, %s, %s, %s, %s)
            """,
            (data.get('title'), data.get('year_of_publish'), data.get('pages'), data.get('description'), data.get('image_file'))
        )
        self.connector.commit()

    def insert_book_into_book_id_author_id(self, data:Book_to_upload) -> None:
        book_id = self.get_book_id_after_post(data)
        author_id = self.get_author_id_from_authors(data)
        self.cursor.execute(
            """
                INSERT INTO book_id_author_id
                VALUES(%s, %s)
            """,
            (book_id, author_id)
        )
        self.commit_close()

    def get_book_id_after_post(self, data: Book_to_upload) -> int:
        self.cursor.execute(
            """
                SELECT book_id FROM books2 
                WHERE title = %s AND year_of_publish = %s AND pages = %s AND description = %s
                ORDER BY book_id DESC LIMIT 1
            """,
            (data.get('title'), data.get('year_of_publish'), data.get('pages'), data.get('description'))
        )
        rows = self.cursor.fetchall()
        book_id = rows[0].get('book_id')
        return book_id
    
    def get_author_id_from_authors(self, data:Book_to_upload) -> int:
        author_id = self.select_author(data)[0].get('author_id')
        return author_id
    
    def select_author(self, data:Book_to_upload) -> Author:
        self.cursor.execute(
            """
                SELECT * FROM authors WHERE full_name = %s
            """,
            (data.get('author'),)
        )
        rows = self.cursor.fetchall()
        return rows

    def change_in_books(self, data:Book) -> None:
        self.cursor.execute(
            """
                UPDATE books2
                SET title = %s, year_of_publish = %s, pages = %s, description = %s, image_base64 = %s
                WHERE book_id = %s
            """,
            (data.get('title'), data.get('year_of_publish'), data.get('pages'), data.get('description'), data.get('image_file'), data.get('id'))
        )
        self.connector.commit()

    def change_in_authors(self, data:Book) -> None:
        author_id = self.get_author_id_from_book_id(book_id=data.get('id'))
        self.cursor.execute(
            """
                UPDATE authors
                SET full_name = %s
                WHERE author_id = %s
            """,
            (data.get('author'), author_id)
        )
        self.commit_close()

    def get_author_id_from_book_id(self, book_id:int) -> int:
        self.cursor.execute(
            """
                SELECT author_id FROM book_id_author_id WHERE book_id = %s
            """,
            (book_id,)
        )
        rows = self.cursor.fetchall()
        author_id = rows[0].get('author_id')
        return author_id
    