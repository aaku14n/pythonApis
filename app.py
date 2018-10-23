from flask import Flask ,jsonify , request
from response import partialResponse, successResponse
import sqlite3

# from flask_restful import Resource, Api
app = Flask(__name__)

# Create some test data for our catalog in the form of a list of dictionaries.

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
# A route to return all of the available entries in our catalog.
@app.route('/book', methods=['POST'])
def api_create():
    if 'name' in request.form:
        name = request.form['name']
    else:
        return partialResponse("Error: No Name field provided. Please specify a Name")
    if 'description' in request.form:
        description = request.form['description']
    else:
        return partialResponse("Error: No description field provided. Please specify an description.")
    if 'imageUrl' in request.form:
        imageUrl = request.form['imageUrl']
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('INSERT into books (name,description,imageUrl) Values (?,?,?)',(name,description,imageUrl)).fetchall()
    conn.commit()
    return successResponse("Successfully inserted")

@app.route('/books', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    return jsonify(all_books)

@app.route('/book', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return partialResponse("Error: No id field provided. Please specify an id.")
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books where id= ?;',(id,)).fetchone()
    
    return jsonify(all_books) 

if __name__ == '__main__':
     app.run(port='5002')
     