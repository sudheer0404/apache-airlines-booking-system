"""
Apache Airlines Seat Booking System, Part B
Database enhanced seat booking system with booking references
"""

import sqlite3
import random
import string

def initialize_database():
#Initializing SQLite database and create bookings table if it doesn't exist
    conn = sqlite3.connect('apache_airlines.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_reference TEXT PRIMARY KEY,
            passport_number TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            seat_row INTEGER NOT NULL,
            seat_column TEXT NOT NULL,
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    print("Database is initialized")
    return conn

def generate_booking_reference(conn):
#Generating unique 8-character booking reference (letters + digits)
    chars = string.ascii_uppercase + string.digits
    ref = ''.join(random.choices(chars, k=8))

#Checking for collisions and regenerate if needed
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM bookings WHERE booking_reference = ?', (ref,))
    if cursor.fetchone():
        return generate_booking_reference(conn)
    return ref

def initialize_seating():
#Creating 80x6 seating grid with aisles (X) and storage areas (S)
    seating = []
    for row in range(1, 81):
        row_seats = []
        for col in range(6):
            if col == 3:
                row_seats.append('X')  # Aisle
            elif row in [77, 78] and col in [3, 4, 5]:
                row_seats.append('S')  # Storage
            else:
                row_seats.append('F')  # Free seat
        seating.append(row_seats)
    return seating

def load_bookings_from_database(seating, conn):
#Loading existing bookings from database into seating matrix
    cursor = conn.cursor()
    cursor.execute('SELECT seat_row, seat_column FROM bookings')
    for row, col in cursor.fetchall():
        seating[row-1][ord(col) - ord('A')] = 'R'  # Mark as reserved
    print(f"Loaded existing bookings")

def get_seat_input():
# Getting and validating seat input from user (format: 1A, 45F, etc.)
    seat = input("Enter seat (e.g., 1D, 42F): ").strip().upper()
    try:
        if len(seat) < 2: raise ValueError
        row, col_letter = int(seat[:-1]), seat[-1]
        if not (1 <= row <= 80 and col_letter in 'ABCDEF'):
            raise ValueError
        return row, ord(col_letter) - ord('A')
    except:
        print("Invalid seat! Please use format like 1A, 45F")
        return None, None

def check_availability(seating, row, col):
# Checking if a specific seat is available for booking
    status = seating[row-1][col]
    seat_name = f"{row}{chr(ord('A') + col)}"
    
    if status == 'F':
        print(f"Yes, {seat_name} AVAILABLE")
        return True
    elif status == 'X':
        print(f" {seat_name} AISLE")
    elif status == 'S':
        print(f"{seat_name} STORAGE")
    else:
        print(f"Sorry, it's {seat_name} BOOKED")
    return False

def book_seat(seating, row, col, conn):
#Booking a seat with passenger details and generate booking reference
    if seating[row-1][col] != 'F':
        print(f"Seat has been already occupied!")
        return False
    
    seat_name = f"{row}{chr(ord('A') + col)}"
    print(f"\nPassenger details for {seat_name}:")
    passport = input("Passport: ").strip()
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    
    if not (passport and first_name and last_name):
        print("All details are required!")
        return False
    
    ref = generate_booking_reference(conn)
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (ref, passport, first_name, last_name, row, chr(ord('A') + col)))
        conn.commit()
        
        seating[row-1][col] = ref  # Store booking reference in seating matrix
        print(f"The seat has been BOOKED {seat_name}, Reference: {ref}")
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def free_seat(seating, row, col, conn):
    """Free a booked seat and remove from database"""
    status = seating[row-1][col]
    seat_name = f"{row}{chr(ord('A') + col)}"
    
    if status in ['F', 'X', 'S']:
        print(f"Cannot free {seat_name}")
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bookings WHERE booking_reference = ?', (status,))
        conn.commit()
        seating[row-1][col] = 'F'  # Mark as free
        print(f"Freed {seat_name}")
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def show_booking_status(seating):
    """Display current seating status with statistics"""
    print("\n" + "="*50)
    print("SEATING STATUS")
    print("="*50)
    
# Displaying seating grid
    for i, row in enumerate(seating):
        print(f"{i+1:3d} " + " ".join(f"{s:4}" if s in ['F','X','S'] else f"{s[:4]}.." for s in row))
    
# Calculating statistics
    total = booked = 0
    for row in seating:
        for seat in row:
            if seat in ['F', 'R'] or len(seat) == 8:  # Count bookable seats
                total += 1
                if seat != 'F': booked += 1
    
    print(f"\nBooked: {booked}, Free: {total-booked}, Occupancy: {booked/total*100:.1f}%")

def search_booking(conn):
#Searching for booking details by reference number
    ref = input("Enter booking reference: ").strip().upper()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE booking_reference = ?', (ref,))
    result = cursor.fetchone()
    
    if result:
        print(f"Found: {result[3]} {result[4]}, Seat: {result[5]}{result[6]}")
    else:
        print("Not found, sorry")

def main():
#Main program loop with menu 
    conn = initialize_database()
    seating = initialize_seating()
    load_bookings_from_database(seating, conn)
    
    while True:
        print("\n1. Check seat\n2. Book seat\n3. Free seat\n4. Show status\n5. Search booking\n6. Exit")
        choice = input("Select your choice: ").strip()
        
        if choice == '1':
            row, col = get_seat_input()
            if row: check_availability(seating, row, col)
        elif choice == '2':
            row, col = get_seat_input()
            if row: book_seat(seating, row, col, conn)
        elif choice == '3':
            row, col = get_seat_input()
            if row: free_seat(seating, row, col, conn)
        elif choice == '4':
            show_booking_status(seating)
        elif choice == '5':
            search_booking(conn)
        elif choice == '6':
            conn.close()
            print("Thank you for using Apache Airlines Booking System")
            break
        else:
            print("Invalid choice entered. Please try again.")

if __name__ == "__main__":
    main()