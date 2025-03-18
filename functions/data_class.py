from dataclasses import dataclass

@dataclass
class Db_config():
    host: str
    user: str
    passwd: str
    database: str

@dataclass
class Book_from_db():
    book_id: int
    title: str
    author: str
    date_of_writing: str
    pages: int
    image: str
    description: str

@dataclass
class Book():
    id: int
    title: str
    author: str
    yearOfPublish: str
    pages: int
    image: str
    description: str

@dataclass
class Author():
    id: int
    full_name: str

@dataclass
class Book_id_Author_id():
    book_id: int
    author_id: int

@dataclass
class Book_name():
    name: str

@dataclass
class Form_data():
    title: str
    author: str
    pages: str
    yearOfPublish: str
    description: str

@dataclass
class File_info():
    image: bytes

@dataclass
class Book_to_upload():
    title: str
    author: str
    pages: str
    year_of_publish: str
    description: str
    image_file: str
