from flask import Flask, request, jsonify
from flask_cors import CORS
from functions.book_service import Book_service


app = Flask(__name__)
CORS(app)

my_db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'sqlpasorddumbbitch22cunt1',
    'database': 'library'
}

@app.route('/api/books')
def api_get_books():
    books = [
        {"id": 1, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky"},
        {"id": 2, "title": "War and Peace", "author": "Leo Tolstoy"}
    ]
    return jsonify(books)

@app.route('/')
def index():
    return 'There aint nothing. Type url'

@app.route('/books', methods = ["GET"])
def get_books():
    return Book_service(my_db_config).get_books()

@app.route('/book/<int:book_id>', methods = ["DELETE"])
def delete_book(book_id:int) -> str:
    return Book_service(my_db_config).delete_book(book_id)

@app.route('/book', methods = ["POST", "PUT"])
def post_put_book():
    data = request.json
    if request.method == 'POST':
        return Book_service(my_db_config).post_book(data)
    elif request.method == 'PUT':
        return Book_service(my_db_config).put_book(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)