# booking_system.py
from models import User # Still used for User object structure from API
from supabase import Client
# Note: iPad and Period objects from models.py are less directly used here,
# as we're dealing with IDs and data from Supabase.

def is_ipad_available(ipad_id: str, date: str, period_id: str, db_client: Client) -> bool:
    """
    Checks if a specific iPad is available for a given date and period using Supabase.
    """
    if not db_client:
        print("Error: Supabase client not provided to is_ipad_available.")
        return False # Or raise an exception

    try:
        response = db_client.table('bookings').select('id').eq('ipad_id', ipad_id).eq('booking_date', date).eq('period_id', period_id).execute()
        if response.data:
            return False # Booking exists, so iPad is not available
        return True # No booking found, iPad is available
    except Exception as e:
        print(f"Error checking iPad availability in Supabase: {e}")
        return False # Treat errors as "not available" or handle more gracefully

def create_booking(user: User, selected_ipad_ids: list[str], date: str, selected_period_ids: list[str], db_client: Client) -> tuple[bool, str, list[dict]]:
    """
    Attempts to create bookings in Supabase for the selected iPads and periods.
    Validates iPad and Period IDs against the database.
    """
    if not db_client:
        return False, "Server error: Database connection not configured.", []

    newly_created_bookings_data = []

    # Validate iPad IDs
    try:
        ipad_validation_response = db_client.table('ipads').select('id').in_('id', selected_ipad_ids).execute()
        valid_db_ipad_ids = {ipad['id'] for ipad in ipad_validation_response.data}
        for ipad_id in selected_ipad_ids:
            if ipad_id not in valid_db_ipad_ids:
                return False, f"Error: iPad with ID '{ipad_id}' not found in database.", []
    except Exception as e:
        print(f"Error validating iPad IDs: {e}")
        return False, "Error validating iPad information.", []

    # Validate Period IDs
    try:
        period_validation_response = db_client.table('periods').select('id').in_('id', selected_period_ids).execute()
        valid_db_period_ids = {period['id'] for period in period_validation_response.data}
        for period_id in selected_period_ids:
            if period_id not in valid_db_period_ids:
                return False, f"Error: Period with ID '{period_id}' not found in database.", []
    except Exception as e:
        print(f"Error validating Period IDs: {e}")
        return False, "Error validating Period information.", []


    # Check availability for all requested slots first
    for ipad_id in selected_ipad_ids:
        for period_id in selected_period_ids:
            if not is_ipad_available(ipad_id, date, period_id, db_client):
                # Fetch details for better error message (optional)
                ipad_desc = ipad_id # Placeholder, could fetch full description
                period_desc = period_id # Placeholder
                return False, f"Booking conflict: iPad {ipad_desc} is already booked for period {period_desc} on {date}.", []

    # All slots are available, prepare records for batch insert
    bookings_to_insert = []
    for ipad_id in selected_ipad_ids:
        for period_id in selected_period_ids:
            bookings_to_insert.append({
                'user_name': user.name,
                'user_email': user.email,
                'booking_date': date,
                'ipad_id': ipad_id,
                'period_id': period_id
            })

    if not bookings_to_insert:
        return False, "No valid bookings to create.", []

    try:
        insert_response = db_client.table('bookings').insert(bookings_to_insert).execute()

        if hasattr(insert_response, 'data') and insert_response.data:
            # The returned data from Supabase insert is usually a list of the inserted records.
            # We might need to join with ipads and periods tables to get full descriptions for the response,
            # or the web_app.py can re-fetch if needed. For simplicity, return what Supabase gives.
            # The structure of items in insert_response.data will be dicts.
            # To match the expected output for web_app.py (which includes descriptions),
            # we might need to do a subsequent query or adjust web_app.py's formatting.
            # For now, let's return the raw inserted data and adapt web_app.py if necessary.

            # For the purpose of the tuple type hint (list[dict]), and to provide consistent data
            # back to web_app.py for its current JSON formatting logic, let's try to fetch the newly created bookings
            # with joined data. This is less efficient (extra SELECT) but simpler for now.
            # A more performant way would be to adjust web_app.py's formatting.

            # Extract IDs of newly created bookings if possible (depends on Supabase return)
            # Assuming insert_response.data gives us dicts with 'id' of the new booking.
            new_booking_ids = [b['id'] for b in insert_response.data if 'id' in b]

            if new_booking_ids:
                # Fetch these new bookings with joined data
                # This select statement is illustrative. The actual join syntax might vary
                # or Supabase Python client might have a more direct way.
                # Using .select() with foreign table hints:
                select_new_q = db_client.table('bookings').select('''
                    id, user_name, user_email, booking_date, ipad_id, period_id,
                    ipads (id, description),
                    periods (id, start_time, end_time)
                ''').in_('id', new_booking_ids).execute()

                if hasattr(select_new_q, 'data') and select_new_q.data:
                    newly_created_bookings_data = select_new_q.data
                else: # Fallback if select fails, use raw insert data (less info)
                    newly_created_bookings_data = insert_response.data
            else: # Fallback if IDs not returned or no data
                 newly_created_bookings_data = insert_response.data


            return True, "Bookings successful.", newly_created_bookings_data
        else:
            # Handle potential errors from Supabase (e.g., unique constraint violation if caught here)
            # The UNIQUE constraint should ideally prevent this stage if is_ipad_available is correct,
            # but good to have a fallback.
            error_msg = "Booking creation failed in database."
            if hasattr(insert_response, 'error') and insert_response.error:
                error_msg += f" DB Error: {insert_response.error.message}"
            print(error_msg) # Log it
            return False, error_msg, []

    except Exception as e:
        print(f"Exception creating bookings in Supabase: {e}")
        # Check if it's a unique constraint violation (specific error codes/messages vary by DB)
        # For Supabase/Postgres, unique violation error code is '23505'
        if "23505" in str(e) or "unique constraint" in str(e).lower(): # Basic check
             return False, "Booking conflict: One or more slots are already booked (database constraint).", []
        return False, f"An unexpected error occurred during booking: {str(e)}", []


def get_all_bookings(db_client: Client) -> list[dict]:
    """
    Retrieves all bookings from Supabase, joining with ipads and periods tables.
    """
    if not db_client:
        print("Error: Supabase client not provided to get_all_bookings.")
        return []
    try:
        # The select string allows specifying columns from foreign tables
        # Syntax: foreign_table_name ( column1, column2, ... )
        # Ensure 'ipads' and 'periods' are the correct names of your foreign tables
        # as referenced by foreign keys in the 'bookings' table.
        response = db_client.table('bookings').select('''
            user_name,
            user_email,
            booking_date,
            ipad_id,
            period_id,
            ipads (id, description),
            periods (id, start_time, end_time)
        ''').order('booking_date', desc=False).order('created_at', desc=False).execute()

        if response.data:
            return response.data
        return []
    except Exception as e:
        print(f"Error fetching all bookings from Supabase: {e}")
        return []

# Old helper functions like get_ipad_by_id, get_period_by_id (that used local data)
# are removed as their functionality is now part of direct DB queries or handled by web_app.py using db_utils.
