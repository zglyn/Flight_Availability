import sqlite3

conn = sqlite3.connect('flights.db')

# Ask the database for EVERY scheduled flight, ignoring dates and airports
query = """
    SELECT F.flight_number, FS.origin_code, FS.dest_code, F.departure_date 
    FROM Flight F
    JOIN FlightService FS ON F.flight_number = FS.flight_number
"""
flights = conn.execute(query).fetchall()

print(f"Total flights found in database: {len(flights)}")
print("-" * 30)

for f in flights:
    print(f"Flight: {f} | Origin: {f} | Dest: {f} | Date: {f}")

conn.close()