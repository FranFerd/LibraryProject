from functions.data_class import Book_from_db, Book
def book_json_response(rows:list[Book_from_db]) -> list[Book]:
    json_response = []
    for row in rows:
        json_response.append({
            'id': row['book_id'],
            'title': row['title'],
            'author': row['author'],
            'yearOfPublish': row['year_of_publish'],
            'pages': row['pages'],
            'image': row['image_base64'],
            'description': row['description']
        })
    return json_response

