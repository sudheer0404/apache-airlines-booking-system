"""
Apache Airlines Seat Booking System - Part A
Burak757 Aircraft Seat Management Application
"""

def initialize_seating():
    """Initialize 80x6 seating layout with aisles and storage areas."""
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

def get_seat_input():
    """Get and validate seat input (e.g., 1A, 45F)."""
    seat = input("Enter seat (e.g., 1A, 45F): ").strip().upper()
    if len(seat) < 2:
        print("Invalid seat format!")
        return None, None
    
    try:
        column_letter = seat[-1]
        row = int(seat[:-1])
        
        if row < 1 or row > 80:
            print("Row must be 1-80!")
            return None, None
        
        if column_letter not in 'ABCDEF':
            print("Column must be A-F!")
            return None, None
        
        return row, ord(column_letter) - ord('A')
    except ValueError:
        print("Invalid seat format!")
        return None, None

def check_availability(seating, row, col):
    """Check if seat is available for booking."""
    seat_status = seating[row-1][col]
    seat_name = f"{row}{chr(ord('A') + col)}"
    
    if seat_status == 'F':
        print(f"✓ Seat {seat_name} is AVAILABLE")
        return True
    elif seat_status == 'R':
        print(f"✗ Seat {seat_name} is BOOKED")
        return False
    else:
        print(f"✗ {seat_name} is {'AISLE' if seat_status == 'X' else 'STORAGE'}")
        return False

def book_seat(seating, row, col):
    """Book a seat if available."""
    seat_status = seating[row-1][col]
    seat_name = f"{row}{chr(ord('A') + col)}"
    
    if seat_status == 'F':
        seating[row-1][col] = 'R'
        print(f"✓ Booked {seat_name}")
        return True
    else:
        print(f"✗ Cannot book {seat_name}")
        return False

def free_seat(seating, row, col):
    """Free a booked seat."""
    seat_status = seating[row-1][col]
    seat_name = f"{row}{chr(ord('A') + col)}"
    
    if seat_status == 'R':
        seating[row-1][col] = 'F'
        print(f"✓ Freed {seat_name}")
        return True
    else:
        print(f"✗ Cannot free {seat_name}")
        return False

def show_booking_status(seating):
    """Display seating chart and statistics."""
    print("\n" + "="*50)
    print("   SEATING CHART - CURRENT STATUS")
    print("="*50)
    print("Row  A  B  C  D  E  F")
    
    for i, row in enumerate(seating):
        print(f"{i+1:3d} " + "  ".join(row))
    
    # Statistics
    total = booked = 0
    for row in seating:
        for seat in row:
            if seat in ['F', 'R']:
                total += 1
                if seat == 'R': booked += 1
    
    print(f"\nBooked: {booked}, Free: {total-booked}, Total: {total}")
    print(f"Occupancy: {(booked/total*100):.1f}%")

def main():
    """Main program loop."""
    seating = initialize_seating()
    
    while True:
        print("\n1. Check availability\n2. Book seat\n3. Free seat\n4. Show status\n5. Exit")
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            row, col = get_seat_input()
            if row and col: check_availability(seating, row, col)
        elif choice == '2':
            row, col = get_seat_input()
            if row and col: book_seat(seating, row, col)
        elif choice == '3':
            row, col = get_seat_input()
            if row and col: free_seat(seating, row, col)
        elif choice == '4':
            show_booking_status(seating)
        elif choice == '5':
            print("Thank you for using Apache Airlines!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()