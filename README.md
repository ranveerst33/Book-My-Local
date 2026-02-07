# BookMyLocal - Local Train Ticket Booking System

BookMyLocal is a web-based application built with Flask that allows users to book local train tickets online. The system provides a convenient way to search for train routes, book tickets, and generate QR codes for ticket verification.

## Features

- **User Authentication**
  - Secure registration and login system
  - Password hashing for security
  - Session management

- **Station Search**
  - Search for train routes between stations
  - Real-time fare calculation based on distance
  - Support for first and second class tickets
  - Return ticket booking option

- **Ticket Management**
  - QR code generation for each ticket
  - Unique PNR number for ticket tracking
  - Ticket validity status tracking
  - View booking history

- **Security Features**
  - Password validation with special character requirements
  - Email validation
  - Protected routes with session management
  - SQL injection prevention

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Additional Libraries**:
  - Werkzeug (Password Hashing)
  - QRCode (Ticket QR Generation)

## Setup Instructions

1. Clone the repository

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Create a MySQL database
   - Import the schema from `setup.sql`
   - Configure database connection in `database.py`

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application at `http://localhost:5000`

## Project Structure

```
BookMyLocal/
├── app.py              # Main application file
├── database.py         # Database configuration
├── requirements.txt    # Python dependencies
├── setup.sql          # Database schema
├── static/            # Static files (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   ├── images/
│   └── qrcodes/       # Generated ticket QR codes
└── templates/         # HTML templates
    ├── layout.html
    ├── homepage.html
    ├── register.html
    ├── login.html
    ├── search.html
    ├── payment.html
    ├── bookings.html
    └── ticket.html
```

