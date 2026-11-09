# Gym Class Auto-Booker

An automated Python script using Selenium that logs into the gym portal, scans the schedule, and automatically books a spot (or joins the waitlist) for selected days (e.g., Wednesday and Friday). It includes a verification system to ensure the booking was successfully registered.

## Key Features
- **Automated Login:** Securely inputs credentials by pulling them from a local `.env` environment variables file.
- **Smart Booking:** Recognizes the current class status (Already Booked, Waitlisted, available for booking) and adjusts its actions accordingly.
- **Automated Verification:** Navigates to the "My Bookings" page and cross-references if the number of newly booked classes matches the system's registered records.
- **Robust Retry Mechanism:** Features built-in custom retry logic, attempting actions up to 7 times in case of network delays or page load errors.

## System Requirements
- Python 3.x
- Selenium (`pip install selenium`)
- python-dotenv (`pip install python-dotenv`)
- Google Chrome browser

## Setup & Installation

1. Create a file named `.env` in the root directory (same folder as `main.py`).
2. Add your credentials inside the `.env` file using the following format:
   ```env
   EMAIL=your_email@gmail.com
   PASSWORD=your_password
   URL=gym_portal_url
