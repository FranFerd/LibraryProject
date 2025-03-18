from flask import Flask, request
import mysql.connector

from functions.data_class import Book_from_db, Book
def book_json_response(rows:list[Book_from_db]) -> list[Book]:
    json_response = []
    for row in rows:
        json_response.append({
            'id': row['book_id'],
            'name': row['title'],
            'dateOfWriting': row['date_of_writing'].strftime('%Y-%m-%d')
        })
    return json_response


app = Flask(__name__)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'sqlpasorddumbbitch22cunt1',
    'database': 'library'
}
connector = mysql.connector.connect(**db_config)
cursor = connector.cursor(dictionary=True, buffered=True)

@app.route('/data', methods=['PUT'])
def post_book():
    data = request.json
    
    rows = cursor.fetchall()
    cursor.close()
    connector.close()
    return {'request_data': data, 'rows_from_db': rows}

if __name__ == '__main__':
    app.run(debug=True)