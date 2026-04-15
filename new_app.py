from flask import Flask, render_template, request
import sqlite3 

app = Flask(__name__)

# Helper func for connection & return row as dict
def db_connection():
    conn = sqlite3.connect("flights.db")
    conn.row_factory = sqlite3.row
    return conn

# The starting page
@app.route('/')
def index():
    return render_template('index.html')

# At the /search page 
@app.route('/search', methods=['POST'])
def search(): 
    origin = request.form['origin']
    dest = request.form['destination']
    start_date = request.form['start_date']
    end_date = request.form['end_date']