# web_app.py
from flask import Flask, request, jsonify, render_template # Added render_template
from models import User
import booking_system
from data import AVAILABLE_IPADS, AVAILABLE_PERIODS
import os

app = Flask(__name__)

# ... (keep existing API routes: /api/ipads, /api/periods, /api/bookings POST, /api/bookings GET) ...
@app.route('/api/ipads', methods=['GET'])
def get_ipads():
    ipads_list = [{"id": ipad.id, "description": ipad.description} for ipad in AVAILABLE_IPADS]
    return jsonify(ipads_list)

@app.route('/api/periods', methods=['GET'])
def get_periods():
    periods_list = [{"id": period.id, "start_time": period.start_time, "end_time": period.end_time} for period in AVAILABLE_PERIODS]
    return jsonify(periods_list)

@app.route('/api/bookings', methods=['POST'])
def create_new_booking():
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

        user = User(name=user_name, email=user_email)

        success, message, created_bookings_details = booking_system.create_booking(
            user=user,
            selected_ipad_ids=selected_ipad_ids,
            date=booking_date,
            selected_period_ids=selected_period_ids
        )

        if success:
            bookings_for_json = [
                {
                    "ipad_id": bk.ipad.id,
                    "ipad_description": bk.ipad.description,
                    "date": bk.date,
                    "period_id": bk.period.id,
                    "period_start_time": bk.period.start_time,
                    "period_end_time": bk.period.end_time,
                    "user_name": bk.user.name
                } for bk in created_bookings_details
            ]
            return jsonify({"success": True, "message": message, "bookings": bookings_for_json}), 201
        else:
            return jsonify({"success": False, "message": message}), 409
    except Exception as e:
        print(f"Error in create_new_booking: {e}") # For server-side logging
        return jsonify({"success": False, "message": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/api/bookings', methods=['GET'])
def get_all_current_bookings():
    all_bookings = booking_system.get_all_bookings()
    bookings_list = [
        {
            "user_name": booking.user.name,
            "user_email": booking.user.email,
            "ipad_id": booking.ipad.id,
            "ipad_description": booking.ipad.description,
            "date": booking.date,
            "period_id": booking.period.id,
            "period_start_time": booking.period.start_time,
            "period_end_time": booking.period.end_time
        } for booking in all_bookings
    ]
    return jsonify(bookings_list)

@app.route('/')
def index():
    return render_template('index.html') # Serves the main HTML page

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    # For Vercel, it's better to not specify host='0.0.0.0' if Vercel's runner handles it.
    # However, for local Docker or similar, 0.0.0.0 is useful.
    # For Vercel, debug=False is also typical in production.
    # Let's keep debug=True for now for easier local testing.
    app.run(debug=True, host='0.0.0.0', port=port)
