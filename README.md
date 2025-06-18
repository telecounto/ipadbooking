# iPad Booking System

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=YOUR_GITHUB_REPO_URL&env=SUPABASE_URL,SUPABASE_KEY&envDescription=Supabase%20URL%20and%20Service%20Key%20for%20the%20booking%20system&project-name=ipad-booking-system&repository-name=my-ipad-booking-system)

## Description

The iPad Booking System is a Python-based application that allows users to book iPads for specific time periods on given dates. It prevents double bookings and provides a list of available iPads and time slots.

This project uses Flask for the web backend and Supabase for data storage. It includes:
1.  A Command-Line Interface (CLI) for all core booking operations (Note: CLI will need updates to use Supabase or be deprecated).
2.  A web-based frontend for user interaction, deployable on Vercel.

## Features

**Core Logic (with Supabase):**
*   Manages iPads and booking periods stored in a Supabase database.
*   Checks for iPad availability against the Supabase database.
*   Prevents double booking using database constraints.
*   Persistent data storage via Supabase.

**Web Interface:**
*   User-friendly interface for all booking operations.
*   Dynamic display of available iPads and periods from Supabase.
*   Visual confirmation and error messages.
*   View all bookings fetched from Supabase.
*   Deployment via Vercel.

## Project Structure

```
ipad-booking-system/
├── web_app.py            # Main Flask application (serves frontend and API)
├── app.py                # Original CLI application (may require Supabase integration or be deprecated)
├── booking_system.py     # Core booking logic (interacts with Supabase)
├── db_utils.py           # Supabase client initialization and data access utilities
├── models.py             # Defines data structures (User class still used)
├── data.py               # Previously held static data, now mainly for reference or seeding ideas
├── requirements.txt      # Python dependencies (Flask, supabase-py)
├── vercel.json           # Vercel deployment configuration
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML page for the web frontend
└── static/
    ├── style.css         # CSS styles
    └── script.js         # Frontend JavaScript logic
```

## Supabase Project Setup

To use this application, you need a Supabase project.

1.  **Create a Supabase Project:**
    *   Go to [supabase.com](https://supabase.com/) and sign up or log in.
    *   Create a new project. Choose a region close to you or your users.
    *   Note down your project's **Name** and **Password** (for the database).

2.  **Get API Credentials:**
    *   Once your project is ready, navigate to **Project Settings** (the gear icon).
    *   Go to the **API** section.
    *   You will find your **Project URL** (this is your `SUPABASE_URL`).
    *   You will also find your `anon` (public) key and `service_role` (secret) key. For backend operations like creating bookings directly from your Python server (bypassing Row Level Security if any), you should use the **`service_role` key**. This key has admin privileges. Treat it like a password and do not expose it publicly. This will be your `SUPABASE_KEY`.

## Database Schema

After setting up your Supabase project, you need to create the necessary tables. You can do this using the Supabase SQL Editor (found under "Database" -> "SQL Editor" in your Supabase project dashboard).

Run the following SQL commands:

**1. `ipads` Table:**
```sql
CREATE TABLE ipads (
    id TEXT PRIMARY KEY,
    description TEXT NOT NULL
);

-- Example Seed Data for ipads (add all iPads as needed):
INSERT INTO ipads (id, description) VALUES
('1', 'iPad 1'),
('2', 'iPad 2'),
('3', 'iPad 3'),
('5', 'iPad 5'),
('6', 'iPad 6'),
('19', 'iPad 19 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)'),
('20', 'iPad 20 Digital Art (After School Mon/Wed) Secondary (Fri Whole Day)'),
-- ... (add all other iPads from the initial list) ...
('61', 'iPad 61 Robotics (After school Tue/Fri)');
```

**2. `periods` Table:**
```sql
CREATE TABLE periods (
    id TEXT PRIMARY KEY,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL
);

-- Example Seed Data for periods:
INSERT INTO periods (id, start_time, end_time) VALUES
('P1', '08:10', '09:00'),
('P2', '09:00', '09:50'),
('P3', '10:00', '10:50'),
('P4', '10:50', '11:40'),
('P5', '11:40', '12:30'),
('P6', '12:30', '13:20'),
('P7', '13:30', '14:20'),
('P8', '14:20', '15:10'),
('P9', '15:30', '16:20');
```

**3. `bookings` Table:**
```sql
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_email TEXT NOT NULL,
    booking_date DATE NOT NULL,
    ipad_id TEXT NOT NULL REFERENCES ipads(id) ON DELETE CASCADE,
    period_id TEXT NOT NULL REFERENCES periods(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (booking_date, ipad_id, period_id) -- Prevents double bookings
);
```
**Note on Seed Data:** You should run the `INSERT INTO` commands for `ipads` and `periods` in the Supabase SQL Editor after creating the tables to populate them with the necessary initial data.

## Environment Variables

The application requires the following environment variables to connect to your Supabase project:

*   `SUPABASE_URL`: Your Supabase project's API URL.
*   `SUPABASE_KEY`: Your Supabase project's `service_role` key.

**For Local Development:**
1.  Create a file named `.env` in the project root directory (this file should NOT be committed to Git).
2.  Add your Supabase credentials to the `.env` file like this:
    ```
    SUPABASE_URL=your_supabase_project_url
    SUPABASE_KEY=your_supabase_service_role_key
    ```
3.  The Python application (when run locally via `python web_app.py`) will need a library like `python-dotenv` to load these variables. Ensure you have it installed (`pip install python-dotenv`) and add `from dotenv import load_dotenv; load_dotenv()` at the beginning of your `web_app.py` (inside the `if __name__ == '__main__':` block or globally if appropriate for your structure).

**For Vercel Deployment:**
These environment variables must be set in your Vercel project settings. See the "Deployment on Vercel" section for more details.

## Setup and Installation

**Prerequisites:**
*   Python 3.x
*   A Supabase account and project (see "Supabase Project Setup").

**Installation:**
1.  Clone this repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  Set up your Supabase database using the SQL schema provided above and populate `ipads` and `periods` tables.
3.  Configure your environment variables for local development (see "Environment Variables").
4.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    (Ensure `python-dotenv` is added to `requirements.txt` if you use it for local development, or instruct users to install it manually for local dev.)

## How to Run

**Web Application (Local Development):**
1.  Ensure your Supabase credentials are set in your `.env` file.
2.  Navigate to the project's root directory.
3.  Run the Flask web application:
    ```bash
    python web_app.py
    ```
4.  Open your browser and go to `http://127.0.0.1:5001` (or the port specified).

**CLI Application:**
*Note: The CLI application (`app.py`) has not been updated to use Supabase. It currently uses in-memory data and will not reflect bookings made via the web interface. It would require significant refactoring to connect to Supabase.*

## Deployment on Vercel

This project is configured for easy deployment on Vercel.

**Using the "Deploy with Vercel" Button:**

1.  **Click the Button:** Click the "Deploy with Vercel" button at the top of this README.
    *   *(Note: You'll need to replace `YOUR_GITHUB_REPO_URL` in the button's link with the actual URL of your public GitHub repository for it to work correctly for others.)*
2.  **Clone Repository:** Vercel will guide you to clone this repository to your GitHub/GitLab/Bitbucket account. You'll give your new repository a name.
3.  **Configure Environment Variables:**
    *   During the setup process, Vercel will prompt you to enter the values for `SUPABASE_URL` and `SUPABASE_KEY`.
    *   Enter the **Project URL** from your Supabase project's API settings as `SUPABASE_URL`.
    *   Enter the **`service_role` key** from your Supabase project's API settings as `SUPABASE_KEY`.
4.  **Deploy:** Vercel will then build and deploy your application. This might take a few minutes.
5.  **Access Your App:** Once deployed, Vercel will provide you with the URL to your live application.

**Manual Deployment Steps (If not using the button, or for an existing fork):**

1.  **Fork the Repository (Optional):**
    *   If you want to maintain your own version or customize the code, fork the original GitHub repository to your own GitHub account.

2.  **Create a New Vercel Project:**
    *   Go to your Vercel dashboard.
    *   Click "Add New..." -> "Project".
    *   Import the Git repository (either the original or your fork). Vercel will detect the `vercel.json` file.

3.  **Configure Project Settings:**
    *   **Framework Preset:** Vercel should automatically detect it as a Python application. If not, you might need to adjust settings, but `vercel.json` should guide it.
    *   **Build & Development Settings:** Usually, these are correctly inferred from `vercel.json` and the presence of `requirements.txt`.
        *   Build Command: Often not needed if `@vercel/python` handles it.
        *   Output Directory: Not typically needed for Flask apps structured this way.
        *   Install Command: `pip install -r requirements.txt` (usually automatic).
    *   **Environment Variables:**
        *   Navigate to your project's settings in Vercel (Settings -> Environment Variables).
        *   Add `SUPABASE_URL` and provide your Supabase project URL.
        *   Add `SUPABASE_KEY` and provide your Supabase `service_role` key.
        *   Ensure these are available to all relevant environments (Production, Preview, Development).

4.  **Deploy:**
    *   Trigger a deployment from your Vercel project dashboard (usually happens automatically on import or after commits to the connected branch).

5.  **Access Your App:**
    *   Once the deployment is complete, Vercel will provide a URL to access your live application.

**Important Notes for Vercel Deployment:**
*   The `vercel.json` file in this repository configures Vercel to use the Python runtime and correctly route requests to the Flask application (`web_app.py`).
*   Ensure your Supabase database tables are created and seeded (for `ipads` and `periods`) as described in the "Database Schema" section before expecting the deployed application to function correctly.
*   The first deployment might take a bit longer as Vercel caches dependencies.

## Future Improvements
...
