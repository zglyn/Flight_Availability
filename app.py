from flask import Flask, render_template, request
import sqlite3 

app = Flask(__name__)

# Helper func for connection & return row as dict
def db_connection():
    conn = sqlite3.connect("flights.db")
    conn.row_factory = sqlite3.Row
    return conn

# The starting page
@app.route('/')
def index():
    return render_template('index.html')

# At the /search page 
@app.route('/search', methods=['POST'])
def search(): 
    # Get the input w request.form
    origin = request.form['origin']
    dest = request.form['destination']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    conn = db_connection()
    
    # SQL Query for flight number, departure date, origin code, dest code, and departure time 
    # Shows even if flight is completely booked 
    query = """ 
    SELECT F.flight_number, F.departure_date, FS.origin_code, FS.dest_code, FS.departure_time
    FROM Flight F
    JOIN FlightService FS ON F.flight_number = FS.flight_number
    WHERE FS.origin_code = ? AND FS.dest_code = ?
      AND F.departure_date BETWEEN ? AND ?
"""
    
    # Return the info from query using the origin, dest, and date info 
    flights = conn.execute(query, (origin, dest, start_date, end_date)).fetchall()
    conn.close()
    
    return render_template('results.html', flights=flights)

# Select a flight and see the available seats & capacity for selected date and flight number combo 
# URL should change based on FN and date
@app.route('/flight/<flight_number>/<departure_date>')
def flight_info(departure_date, flight_number): 
    conn = db_connection() 
    
    # SQL Query to get the available seats and capacity 
    # Seats = total capacity - booked 
    # Left join to show flights wit no bookings 
    query = """
        SELECT A.capacity, (A.capacity - COUNT(B.pid)) AS available_seats
        FROM Flight F
        JOIN Aircraft A ON F.plane_type = A.plane_type
        LEFT JOIN Booking B ON F.flight_number = B.flight_number 
                           AND F.departure_date = B.departure_date
        WHERE F.flight_number = ? AND F.departure_date = ?
        GROUP BY A.capacity
    """
    details = conn.execute(query, (flight_number, departure_date)).fetchone()
    conn.close()
    
    return render_template('details.html', details=details, 
                           flight_number=flight_number, date=departure_date)

if __name__ == '__main__':
    app.run(debug=True)