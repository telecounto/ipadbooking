# app.py
from models import User
from data import AVAILABLE_IPADS, AVAILABLE_PERIODS
import booking_system # To avoid circular imports if booking_system also imported app features

def display_ipads():
    print("\n--- Available iPads ---")
    for ipad in AVAILABLE_IPADS:
        print(f"ID: {ipad.id} - {ipad.description}")
    print("-----------------------")

def display_periods():
    print("\n--- Available Periods ---")
    for period in AVAILABLE_PERIODS:
        print(f"ID: {period.id} - {period.start_time} to {period.end_time}")
    print("-------------------------")

def get_user_input_for_selection(prompt_message: str, valid_ids: list[str]) -> list[str]:
    """Generic function to get comma-separated ID selections from the user."""
    selected_items = []
    while True:
        user_input_str = input(prompt_message).strip()
        if not user_input_str:
            print("Input cannot be empty. Please enter valid IDs or 'cancel'.")
            continue
        if user_input_str.lower() == 'cancel':
            return [] # Empty list indicates cancellation by user

        raw_ids = [item_id.strip() for item_id in user_input_str.split(',')]

        invalid_ids_found = [item_id for item_id in raw_ids if item_id not in valid_ids]

        if invalid_ids_found:
            print(f"Error: Invalid IDs entered: {', '.join(invalid_ids_found)}. Please try again.")
            print(f"Valid IDs are: {', '.join(valid_ids)}")
        else:
            selected_items = raw_ids
            break
    return selected_items

def main_menu():
    print("Welcome to the iPad Booking System!")

    while True:
        print("\nWhat would you like to do?")
        print("1. Make a new booking")
        print("2. View all bookings")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            make_new_booking()
        elif choice == '2':
            view_all_bookings()
        elif choice == '3':
            print("Thank you for using the iPad Booking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def make_new_booking():
    print("\n--- New Booking ---")

    # 1. Get User Information
    user_name = input("Enter your name: ").strip()
    while not user_name:
        print("Name cannot be empty.")
        user_name = input("Enter your name: ").strip()

    user_email = input("Enter your email: ").strip()
    while not user_email: # Basic validation, could be more complex
        print("Email cannot be empty.")
        user_email = input("Enter your email: ").strip()

    user = User(name=user_name, email=user_email)

    # 2. Get Date
    # TODO: Add date validation (e.g., format YYYY-MM-DD, not in the past)
    booking_date = input("Enter booking date (YYYY-MM-DD): ").strip()
    while not booking_date: # Basic validation
        print("Date cannot be empty.")
        booking_date = input("Enter booking date (YYYY-MM-DD): ").strip()

    # 3. Select iPads
    display_ipads()
    valid_ipad_ids = [ipad.id for ipad in AVAILABLE_IPADS]
    selected_ipad_ids = []
    while not selected_ipad_ids:
        selected_ipad_ids = get_user_input_for_selection(
            "Enter iPad IDs to book (comma-separated, e.g., 1,2,19) or type 'cancel': ",
            valid_ipad_ids
        )
        if not selected_ipad_ids and input("No iPads selected. Cancel booking? (yes/no): ").lower() == 'yes':
            print("Booking cancelled.")
            return

    if not selected_ipad_ids: # If 'cancel' was typed in get_user_input_for_selection
        print("Booking process cancelled by user.")
        return

    # 4. Select Periods
    display_periods()
    valid_period_ids = [period.id for period in AVAILABLE_PERIODS]
    selected_period_ids = []
    while not selected_period_ids:
        selected_period_ids = get_user_input_for_selection(
            "Enter Period IDs to book (comma-separated, e.g., P1,P2) or type 'cancel': ",
            valid_period_ids
        )
        if not selected_period_ids and input("No periods selected. Cancel booking? (yes/no): ").lower() == 'yes':
            print("Booking cancelled.")
            return

    if not selected_period_ids: # If 'cancel' was typed in get_user_input_for_selection
        print("Booking process cancelled by user.")
        return

    # 5. Display Summary and Confirm
    print("\n--- Booking Summary ---")
    print(f"Name: {user.name}")
    print(f"Email: {user.email}")
    print(f"Date: {booking_date}")
    print(f"Selected iPad IDs: {', '.join(selected_ipad_ids)}")
    # Fetch full iPad descriptions for summary
    selected_ipad_descs = [ipad.description for ipad in AVAILABLE_IPADS if ipad.id in selected_ipad_ids]
    for desc in selected_ipad_descs:
        print(f"  - {desc}")
    print(f"Selected Period IDs: {', '.join(selected_period_ids)}")
    # Fetch full Period details for summary
    selected_period_details = [f"{p.id} ({p.start_time}-{p.end_time})" for p in AVAILABLE_PERIODS if p.id in selected_period_ids]
    for detail in selected_period_details:
        print(f"  - {detail}")
    print("-----------------------")

    confirm = input("Confirm booking? (yes/no): ").strip().lower()
    if confirm == 'yes':
        success, message, created_bookings = booking_system.create_booking(
            user=user,
            selected_ipad_ids=selected_ipad_ids,
            date=booking_date,
            selected_period_ids=selected_period_ids
        )
        print(f"\n{message}")
        if success:
            print("Successfully created bookings:")
            for bk in created_bookings:
                print(f"  - iPad {bk.ipad.id} for Period {bk.period.id} on {bk.date} for {bk.user.name}")
        else:
            print("Booking failed.")
    else:
        print("Booking cancelled by user.")

def view_all_bookings():
    print("\n--- All Bookings ---")
    all_bookings = booking_system.get_all_bookings()
    if not all_bookings:
        print("No bookings found.")
    else:
        for booking in all_bookings:
            print(f"User: {booking.user.name}, Email: {booking.user.email}, "
                  f"iPad ID: {booking.ipad.id}, Description: {booking.ipad.description}, "
                  f"Date: {booking.date}, Period: {booking.period.id} ({booking.period.start_time}-{booking.period.end_time})")
    print("--------------------")

if __name__ == "__main__":
    main_menu()
