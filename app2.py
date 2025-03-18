from flask import Flask, request
from flask_cors import CORS
from functions.book_author_service import Book_author_service
from werkzeug.formparser import parse_form_data

app = Flask(__name__)
CORS(app)  # Global CORS configuration

my_db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'sqlpasorddumbbitch22cunt1',
    'database': 'library'
}

@app.route('/')
def index():
    return 'There aint nothing. Type url'

@app.route('/books', methods=["GET"])
def get_books():
    return Book_author_service(my_db_config).get_books()

@app.route('/book-delete/<int:book_id>', methods=["DELETE"])
def delete_book(book_id: int):
    return Book_author_service(my_db_config).delete_book(book_id)

@app.route('/book-update', methods=["PUT"])
def put_book():
    form_data = request.form.to_dict()
    form_files = request.files.get("image")
    return Book_author_service(my_db_config).put_book(form_data, form_files)

@app.route('/book-search', methods=["GET"])
def get_book_by_name():
    data = request.args.get('name')
    return Book_author_service(my_db_config).get_book_by_name(data)

@app.route('/upload', methods=["POST"]) 
def upload_book_with_image():
    form_data = request.form.to_dict()
    form_files = request.files.get("image")
    return Book_author_service(my_db_config).upload_book_with_image(form_data, form_files)

@app.route('/book-id', methods = ["POST"])
def get_book_id():
    form_data = request.form.to_dict()
    form_files = request.files.get("image")
    return Book_author_service(my_db_config).get_book_id_after_post(form_data, form_files)


if __name__ == '__main__':
    app.run(debug=True, port=5000)