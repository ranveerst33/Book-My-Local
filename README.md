Mumbai Local Train Ticket Booking System

Description:
A web-based Mumbai local train ticket booking system developed using Python Flask and MySQL to simplify ticket booking across Mumbai’s suburban railway network. The application allows users to book tickets digitally, reducing queues and improving commuter convenience through a secure and user-friendly interface.

Features:
- Secure user authentication with password hashing
- Real-time fare calculation based on station distance
- First-class and second-class ticket booking
- Return ticket booking option
- Unique PNR generation for every booking
- QR code generation for ticket verification
- Ticket validity tracking
- Booking history dashboard for users
- Session management for security
- Protection against SQL injection

Tech Stack:
Frontend: HTML, CSS, JavaScript  
Backend: Python (Flask)  
Database: MySQL  
Libraries/Tools: Flask, MySQL Connector, QR Code Generator, Werkzeug

Installation and Setup:

1. Clone the repository
git clone https://github.com/ranveerst33/mumbai-train-booking-system.git
cd mumbai-train-booking-system

2. Create virtual environment
python -m venv venv
source venv/bin/activate   (Windows: venv\Scripts\activate)

3. Install dependencies
pip install flask mysql-connector-python qrcode

4. Setup MySQL database
- Create a MySQL database
- Import the SQL file provided in project
- Update database credentials in app.py

5. Run application
python app.py

6. Open in browser
http://127.0.0.1:5000

Learning Outcomes:
- Full-stack web development using Flask
- Database design and MySQL integration
- Secure authentication and session handling
- Implementation of real-world booking system logic
- QR code and PNR-based ticket verification

Future Enhancements:
- Online payment gateway integration
- Admin dashboard
- Mobile responsive UI
- Live train schedule API
- Email/SMS ticket confirmation

Author:
Ranveer Singh Thakur
GitHub: https://github.com/ranveerst33  
LinkedIn: https://www.linkedin.com/in/ranveer-singh-thakur-2721463ab/
