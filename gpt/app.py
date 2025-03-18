from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'user': 'root',
    'password': 'sqlpasorddumbbitch22cunt1',
    'host': 'localhost',
    'database': 'crud_app'
}

@app.route('/')
def index():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    item_name = request.form.get('name')
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO items(name) VALUES(%s)", (item_name,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

@app.route('/book', methods=["POST"])
def add_book():
    print(request.json)
    return request.json

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    if request.method == 'POST':
        item_name = request.form.get('name')
        cursor.execute("UPDATE items SET name=%s WHERE id=%s", (item_name, item_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM items WHERE id=%s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit.html', item=item)

@app.route('/delete/<int:item_id>')
def delete(item_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM items WHERE id=%s", (item_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)