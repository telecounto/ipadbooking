# web_app.py
from flask import Flask, request, jsonify, render_template
from models import User
import booking_system
# Remove: from data import AVAILABLE_IPADS, AVAILABLE_PERIODS
from db_utils import get_all_ipads_from_db, get_all_periods_from_db, supabase_client # Import client for other parts
import os

app = Flask(__name__)

@app.before_first_request
def check_supabase_connection():
    if not supabase_client:
        # This is a simple check. In a real app, you might want more robust health checks
        # or prevent the app from starting if Supabase isn't configured.
        print("CRITICAL: Supabase client not initialized. Check environment variables.")
        # Depending on desired behavior, you could raise an exception here
        # or allow the app to run with Supabase-dependent features failing.

@app.route('/api/ipads', methods=['GET'])
def get_ipads():
    if not supabase_client:
        return jsonify({"error": "Supabase client not initialized. Check server configuration."}), 500
    ipads_list = get_all_ipads_from_db()
    return jsonify(ipads_list)

@app.route('/api/periods', methods=['GET'])
def get_periods():
    if not supabase_client:
        return jsonify({"error": "Supabase client not initialized. Check server configuration."}), 500
    periods_list = get_all_periods_from_db()
    return jsonify(periods_list)

@app.route('/api/available_slots', methods=['GET'])
def get_available_slots():
    if not supabase_client:
        return jsonify({"error": "Supabase client not initialized. Check server configuration."}), 500

    date = request.args.get('date')
    if not date:
        return jsonify({"error": "Date parameter is required."}), 400

    available_slots = booking_system.get_available_slots_for_date(date, db_client=supabase_client)
    return jsonify(available_slots)

@app.route('/api/bookings', methods=['POST'])
def create_new_booking():
    if not supabase_client: # Ensure client is available for booking_system
        return jsonify({"success": False, "message": "Server error: Database connection not configured."}), 500
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Invalid input: No data provided."}), 400

        user_name = data.get('userName')
        user_email = data.get('userEmail')
        selected_ipad_ids = data.get('ipadIds')
        booking_date = data.get('date')
        selected_period_ids = data.get('periodIds')

        if not all([user_name, user_email, selected_ipad_ids, booking_date, selected_period_ids]):
            return jsonify({"success": False, "message": "Invalid input: Missing required fields."}), 400

        if not isinstance(selected_ipad_ids, list) or not isinstance(selected_period_ids, list):
            return jsonify({"success": False, "message": "Invalid input: ipadIds and periodIds must be lists."}), 400

        user = User(name=user_name, email=user_email) # User model is still used for structure

        # booking_system will need to be refactored to use supabase_client
        success, message, created_bookings_details = booking_system.create_booking(
            user=user,
            selected_ipad_ids=selected_ipad_ids,
            date=booking_date,
            selected_period_ids=selected_period_ids,
            db_client=supabase_client # Pass client to booking_system
        )

        if success:
            # Format might change based on what create_booking returns from Supabase
            bookings_for_json = [
                {
                    "ipad_id": bk.get("ipad_id"), # Assuming create_booking will return dicts
                    "ipad_description": bk.get("ipad_description", ""), # Need to fetch or join
                    "date": bk.get("booking_date"),
                    "period_id": bk.get("period_id"),
                    "period_start_time": bk.get("period_start_time", ""), # Need to fetch or join
                    "period_end_time": bk.get("period_end_time", ""),   # Need to fetch or join
                    "user_name": bk.get("user_name")
                } for bk in created_bookings_details
            ]
            return jsonify({"success": True, "message": message, "bookings": bookings_for_json}), 201
        else:
            return jsonify({"success": False, "message": message}), 409 # Conflict or other error
    except Exception as e:
        print(f"Error in create_new_booking: {e}")
        return jsonify({"success": False, "message": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/api/bookings', methods=['GET'])
def get_all_current_bookings():
    if not supabase_client: # Ensure client is available for booking_system
        return jsonify({"error": "Server error: Database connection not configured."}), 500

    # booking_system will need to be refactored to use supabase_client
    all_bookings = booking_system.get_all_bookings(db_client=supabase_client) # Pass client

    # The structure of 'all_bookings' will now be a list of dicts from Supabase.
    # It might already include joined data for ipad_description and period times if query is designed well.
    # For now, assume it's similar to the previous structure and adjust if needed after refactoring booking_system.
    # This part will likely need adjustment after booking_system.py is refactored.
    bookings_list = [
        {
            "user_name": booking.get("user_name"),
            "user_email": booking.get("user_email"),
            "ipad_id": booking.get("ipad_id"),
            "ipad_description": booking.get("ipads", {}).get("description") if booking.get("ipads") else None, # Example if joining
            "date": booking.get("booking_date"),
            "period_id": booking.get("period_id"),
            "period_start_time": booking.get("periods", {}).get("start_time") if booking.get("periods") else None, # Example if joining
            "period_end_time": booking.get("periods", {}).get("end_time") if booking.get("periods") else None, # Example if joining
        } for booking in all_bookings
    ]
    return jsonify(bookings_list)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Ensure environment variables are loaded for local development, e.g., using python-dotenv
    # For Vercel, these will be set in the project settings.
    # from dotenv import load_dotenv
    # load_dotenv()

    # Re-initialize client here if using dotenv and it wasn't available at module load time
    # This is a bit tricky with global client. Better to ensure env vars are set before running.
    # For simplicity, assume env vars are set.

    if not supabase_client:
        print("Failed to initialize Supabase client. Ensure SUPABASE_URL and SUPABASE_KEY are set.")
        # Optionally exit if client is essential for local run:
        # import sys
        # sys.exit(1)

    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
