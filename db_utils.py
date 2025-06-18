# db_utils.py
from supabase import create_client, Client
import os

def init_supabase_client() -> Client | None:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY") # Should be service_role key for backend operations
    if not url or not key:
        print("Error: SUPABASE_URL and SUPABASE_KEY environment variables are required.")
        return None
    try:
        return create_client(url, key)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        return None

# Global client instance, initialized once
supabase_client = init_supabase_client()

def get_all_ipads_from_db() -> list[dict]:
    if not supabase_client:
        return []
    try:
        response = supabase_client.table('ipads').select('id, description').execute()
        if response.data:
            return response.data
        print(f"No data or error fetching iPads: {getattr(response, 'error', 'No error attribute')}")
        return []
    except Exception as e:
        print(f"Exception fetching iPads: {e}")
        return []

def get_all_periods_from_db() -> list[dict]:
    if not supabase_client:
        return []
    try:
        response = supabase_client.table('periods').select('id, start_time, end_time').execute()
        if response.data:
            return response.data
        print(f"No data or error fetching periods: {getattr(response, 'error', 'No error attribute')}")
        return []
    except Exception as e:
        print(f"Exception fetching periods: {e}")
        return []

# Add other database interaction functions here in the next step
# e.g., for checking availability, creating bookings, getting all bookings.
