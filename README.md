# iPad Booking System

## Description

The iPad Booking System is a Python-based application that allows users to book iPads for specific time periods on given dates. It prevents double bookings and provides a list of available iPads and time slots.

This project currently includes:
1.  A Command-Line Interface (CLI) for all core booking operations.
2.  (Planned) A web-based frontend for easier user interaction, deployable on Vercel.

## Features

**Core Logic:**
*   Manages a list of iPads with unique IDs and descriptions.
*   Manages predefined booking periods.
*   Checks for iPad availability for a given date and period.
*   Prevents double booking of the same iPad for the same date/period.
*   In-memory data storage (bookings are reset when the application stops).

**Command-Line Interface (CLI):**
*   Enter user name and email.
*   Select a booking date.
*   View and select from a list of available iPads.
*   View and select from a list of available time periods.
*   Receive confirmation or error messages for booking attempts.
*   View all current bookings.

**(Planned) Web Frontend Features:**
*   User-friendly interface for all booking operations.
*   Dynamic display of available iPads and periods.
*   Visual confirmation and error messages.
*   View all bookings through the web interface.
*   Deployment via Vercel.

## Project Structure

```
ipad-booking-system/
├── app.py                # Main CLI application entry point
├── booking_system.py     # Core booking logic (availability checks, booking creation)
├── data.py               # Contains predefined lists of iPads and time periods
├── models.py             # Defines data structures (User, iPad, Period, Booking)
├── README.md             # This file
├── templates/            # (Planned) HTML templates for web frontend
└── static/               # (Planned) CSS and JavaScript files for web frontend
```

## Setup and Installation

**Prerequisites:**
*   Python 3.x

**Installation:**
1.  Clone this repository (or download the source files).
2.  No external Python libraries are required for the CLI version beyond the standard library.
    ```bash
    # No pip install needed for the current CLI version
    ```
3.  (For planned Web App) Dependencies for the web framework (e.g., Flask) will be listed here. A `requirements.txt` file will be provided.

## How to Run

**CLI Application:**
1.  Navigate to the project's root directory in your terminal.
2.  Run the CLI application using Python:
    ```bash
    python app.py
    ```
3.  Follow the on-screen prompts to make or view bookings.

**(Planned) Web Application:**
*   Instructions for running the web application locally and accessing it via a browser will be added here.

## Future Improvements (from previous planning)
*   **Persistent Storage:** Implement database storage (e.g., SQLite, PostgreSQL) for bookings so data persists between sessions.
*   **User Authentication:** Add user accounts and authentication for a more secure system.
*   **Admin Interface:** Develop an admin panel to manage iPads, users, and all bookings.
*   **Advanced iPad Rules:** Implement special booking rules for iPads designated for specific clubs or activities (e.g., Digital Art, E-Sports, Robotics restricting by day/time or user group).
*   **Email Notifications:** Send email confirmations to users upon successful booking.
*   **Edit/Cancel Bookings:** Allow users to modify or cancel their existing bookings.
*   **Enhanced UI/UX:** Develop a more polished and feature-rich web interface.
*   **Date/Time Validation:** More robust validation for dates (e.g., no booking in the past, proper date formats).
*   **API Documentation:** If a more extensive API is built, provide clear documentation (e.g., using Swagger/OpenAPI).
*   **Testing:** Add comprehensive unit and integration tests.

```
