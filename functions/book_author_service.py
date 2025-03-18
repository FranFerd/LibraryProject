from functions.books_json_response_func import book_json_response
from functions.data_class import Db_config, Book, Form_data, File_info
from functions.mysql_code import Mysql_code
from flask import jsonify
import base64



class Book_author_service(): 
    def __init__(self, db_config:Db_config) -> None:
        # self.db_config = db_config
        self.repository = Mysql_code(db_config)
        
    def get_books(self) -> list[Book]:
        rows = self.repository.select_all_books_and_author()
        return book_json_response(rows)
    
    def delete_book(self, book_id:int) -> str:
        self.repository.delete_from_book_id_author_id(book_id)
        self.repository.delete_from_books(book_id)
        # author_id = Mysql_code(self.db_config).get_author_id_from_book_id(book_id)
        # Mysql_code(self.db_config).delete_from_authors(author_id)
        return 'Book deleted successfully'
    
    def get_book_by_name(self, book_name: str):
        rows = self.repository.get_book_by_name(book_name)
        return book_json_response(rows)
    
    def upload_book_with_image(self, form_data: Form_data, form_files: File_info) -> str:

        file_content = form_files.read()
        base64_encoded = base64.b64encode(file_content).decode('utf-8')


        data = {
            "title": form_data.get("title"),
            "author": form_data.get("author"),
            "pages": form_data.get("pages"),
            "year_of_publish": form_data.get("yearOfPublish"),
            "description": form_data.get("description"),
            "image_file": base64_encoded
        }

        author = self.repository.select_author(data)
        if author == []:
            self.repository.insert_new_author(data)
        self.repository.insert_book_into_books(data)
        self.repository.insert_book_into_book_id_author_id(data)
        return 'Book uploaded succussfully'
    
    def put_book(self, form_data: Form_data, form_files: File_info) -> str:
        if form_files:
            file_content = form_files.read()
            base64_encoded = base64.b64encode(file_content).decode('utf-8')
        else:
            base64_encoded = form_data.get('image')

        data = {
            "id": form_data.get("id"),
            "title": form_data.get("title"),
            "author": form_data.get("author"),
            "pages": form_data.get("pages"),
            "year_of_publish": form_data.get("yearOfPublish"),
            "description": form_data.get("description"),
            "image_file": base64_encoded
        }
        self.repository.change_in_books(data)
        self.repository.change_in_authors(data)
        return 'Book changed successfully'
    
    def get_book_id_after_post(self, form_data: Form_data, form_files: File_info) -> str:
        file_content = form_files.read()
        base64_encoded = base64.b64encode(file_content).decode('utf-8')


        data = {
            "title": form_data.get("title"),
            "author": form_data.get("author"),
            "pages": form_data.get("pages"),
            "year_of_publish": form_data.get("yearOfPublish"),
            "description": form_data.get("description"),
            "image_file": base64_encoded
        }

        book_id = self.repository.get_book_id_after_post(data)
        return jsonify({"bookId" : book_id})