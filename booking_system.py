# booking_system.py
from models import User, iPad, Period, Booking
from data import AVAILABLE_IPADS, AVAILABLE_PERIODS # Assuming these might be useful for validation or listing

# In-memory list to store bookings
# In a real application, this would be a database
_bookings: list[Booking] = []

def is_ipad_available(ipad_id: str, date: str, period_id: str) -> bool:
    """
    Checks if a specific iPad is available for a given date and period.

    Args:
        ipad_id: The ID of the iPad to check.
        date: The date of the booking (e.g., "YYYY-MM-DD").
        period_id: The ID of the time period.

    Returns:
        True if the iPad is available, False otherwise.
    """
    for booking in _bookings:
        if booking.ipad.id == ipad_id and            booking.date == date and            booking.period.id == period_id:
            return False  # iPad is already booked for this date and period
    return True

def get_ipad_by_id(ipad_id: str) -> iPad | None:
    """Helper function to find an iPad object by its ID."""
    for ipad_obj in AVAILABLE_IPADS:
        if ipad_obj.id == ipad_id:
            return ipad_obj
    return None

def get_period_by_id(period_id: str) -> Period | None:
    """Helper function to find a Period object by its ID."""
    for period_obj in AVAILABLE_PERIODS:
        if period_obj.id == period_id:
            return period_obj
    return None

def create_booking(user: User, selected_ipad_ids: list[str], date: str, selected_period_ids: list[str]) -> tuple[bool, str, list[Booking]]:
    """
    Attempts to create bookings for the selected iPads and periods.

    Args:
        user: The User object making the booking.
        selected_ipad_ids: A list of IDs of the iPads to book.
        date: The date for the bookings (e.g., "YYYY-MM-DD").
        selected_period_ids: A list of IDs of the time periods to book.

    Returns:
        A tuple containing:
        - bool: True if all bookings were successful, False otherwise.
        - str: A message indicating success or detailing the first conflict found.
        - list[Booking]: A list of successfully created Booking objects. Empty if any part fails.
    """
    newly_created_bookings = []

    # Validate iPad and Period IDs first
    for ipad_id in selected_ipad_ids:
        if get_ipad_by_id(ipad_id) is None:
            return False, f"Error: iPad with ID '{ipad_id}' not found.", []

    for period_id in selected_period_ids:
        if get_period_by_id(period_id) is None:
            return False, f"Error: Period with ID '{period_id}' not found.", []

    for ipad_id in selected_ipad_ids:
        ipad_obj = get_ipad_by_id(ipad_id) # We know it exists from validation above
        for period_id in selected_period_ids:
            period_obj = get_period_by_id(period_id) # We know it exists

            if not is_ipad_available(ipad_id, date, period_id):
                # If any slot is unavailable, fail the entire transaction for simplicity.
                # A more complex system might allow partial bookings.
                return False, f"Booking conflict: iPad {ipad_id} is already booked for period {period_id} on {date}.", []

            # If we were to create bookings one by one and add them,
            # we'd need to handle rollbacks if a later one fails.
            # For now, we check all first, then create.

    # All checks passed, now create the bookings
    for ipad_id in selected_ipad_ids:
        ipad_obj = get_ipad_by_id(ipad_id)
        for period_id in selected_period_ids:
            period_obj = get_period_by_id(period_id)

            booking = Booking(user=user, ipad=ipad_obj, date=date, period=period_obj)
            newly_created_bookings.append(booking)

    _bookings.extend(newly_created_bookings)
    return True, "Bookings successful.", newly_created_bookings

def get_all_bookings() -> list[Booking]:
    """Returns a list of all current bookings."""
    return list(_bookings) # Return a copy

# Example usage (optional, for testing booking_system.py directly)
if __name__ == '__main__':
    # Create a dummy user
    test_user = User(name="Test User", email="test@example.com")

    # Attempt to book iPad "1" for Period "P1" on "2024-01-01"
    print("Attempting first booking...")
    success, message, created_bks = create_booking(user=test_user, selected_ipad_ids=["1"], date="2024-01-01", selected_period_ids=["P1"])
    print(f"Success: {success}, Message: {message}, Bookings: {created_bks}")

    # Attempt to book the same slot again
    print("\nAttempting conflicting booking...")
    success, message, created_bks = create_booking(user=test_user, selected_ipad_ids=["1"], date="2024-01-01", selected_period_ids=["P1"])
    print(f"Success: {success}, Message: {message}, Bookings: {created_bks}")

    # Attempt to book multiple iPads and periods
    print("\nAttempting multiple bookings (non-conflicting)...")
    success, message, created_bks = create_booking(user=test_user, selected_ipad_ids=["2", "3"], date="2024-01-01", selected_period_ids=["P1", "P2"])
    print(f"Success: {success}, Message: {message}, Bookings: {created_bks}")

    # Attempt to book one that is taken and one that is not
    print("\nAttempting mixed bookings (one conflicting)...")
    # iPad "2" for "P1" on "2024-01-01" is now taken from the previous multi-booking.
    # iPad "5" for "P1" on "2024-01-01" should be available.
    success, message, created_bks = create_booking(user=test_user, selected_ipad_ids=["2", "5"], date="2024-01-01", selected_period_ids=["P1"])
    print(f"Success: {success}, Message: {message}, Bookings: {created_bks}")

    print("\nAll bookings made:")
    for bk in get_all_bookings():
        print(bk)

    print("\nChecking availability for iPad 1, Period P1 on 2024-01-01 (should be False):")
    print(is_ipad_available(ipad_id="1", date="2024-01-01", period_id="P1"))

    print("\nChecking availability for iPad 1, Period P2 on 2024-01-01 (should be True):")
    print(is_ipad_available(ipad_id="1", date="2024-01-01", period_id="P2"))
