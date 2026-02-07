from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import qrcode
import random
import string
from database import get_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Create directory for QR codes if not exists
os.makedirs("static/qrcodes", exist_ok=True)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email already registered", "danger")
                return redirect(url_for('register'))

            cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                           (first_name, last_name, email, hashed_password))
            conn.commit()
            flash("Registration successful!", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash("Something went wrong!", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = f"{user['first_name']} {user['last_name']}"
                session['email'] = user['email']
                flash("Login successful", "success")
                return redirect(url_for('search'))
            else:
                flash("Invalid email or password", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT station_id, station_name, station_code FROM stations")
    stations = cursor.fetchall()

    if request.method == 'POST':
        source_name = request.form.get('source_station')
        dest_name = request.form.get('destination_station')

        source_id = next((s['station_id'] for s in stations if f"{s['station_name']} ({s['station_code']})" == source_name), None)
        destination_id = next((s['station_id'] for s in stations if f"{s['station_name']} ({s['station_code']})" == dest_name), None)

        if not source_id or not destination_id:
            flash("Please select valid stations from the list", "danger")
            return redirect(url_for('search'))

        if source_id == destination_id:
            flash("Source and destination cannot be the same", "danger")
            return redirect(url_for('search'))

        cursor.execute("SELECT * FROM stations WHERE station_id = %s", (source_id,))
        source = cursor.fetchone()

        cursor.execute("SELECT * FROM stations WHERE station_id = %s", (destination_id,))
        destination = cursor.fetchone()

        if not source or not destination:
            flash("One or both of the selected stations are invalid", "danger")
            return redirect(url_for('search'))

        # Calculate base fare
        distance_diff = abs(destination['distance'] - source['distance'])
        fare = abs(destination['fare'] - source['fare'])
        fare = fare if fare > 5 else 5

        # Apply fare multipliers
        ticket_class = request.form.get('ticket_class', 'second')
        if ticket_class == 'first':
            fare *= 2

        if request.form.get('return_ticket'):
            fare *= 2

        qr_content = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        qr_path = f"static/qrcodes/{qr_content}.png"
        qrcode.make(qr_content).save(qr_path)

        session['booking_details'] = {
            'source_id': source_id,
            'destination_id': destination_id,
            'fare': fare,
            'booking_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'qr_code_path': qr_path,
            'ticket_class': ticket_class,
            'is_return': bool(request.form.get('return_ticket'))
        }

        cursor.close()
        conn.close()
        return redirect(url_for('payment'))

    cursor.close()
    conn.close()
    return render_template('search.html', stations=stations)

@app.route('/payment')
def payment():
    if 'booking_details' not in session:
        return redirect(url_for('search'))
    return render_template('payment.html', fare=session['booking_details']['fare'], qr_code_path=session['booking_details']['qr_code_path'])

@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    if 'booking_details' not in session or 'user_id' not in session:
        return redirect(url_for('search'))

    booking = session.pop('booking_details')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (user_id, source_station_id, destination_station_id, booking_time, fare, qr_code_path, ticket_class, is_return)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (session['user_id'], booking['source_id'], booking['destination_id'], booking['booking_time'], booking['fare'], booking['qr_code_path'], booking['ticket_class'], booking['is_return']))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Ticket booked successfully!", "success")
    return redirect(url_for('bookings'))

@app.route('/bookings')
def bookings():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.pnr, s1.station_name AS source_name, s1.station_code AS source_code,
               s2.station_name AS destination_name, s2.station_code AS destination_code,
               b.booking_time, b.fare, b.qr_code_path, b.ticket_class, b.is_return
        FROM bookings b
        JOIN stations s1 ON b.source_station_id = s1.station_id
        JOIN stations s2 ON b.destination_station_id = s2.station_id
        WHERE b.user_id = %s
        ORDER BY b.booking_time DESC
    """, (session['user_id'],))
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()

    for b in bookings:
        booking_time = datetime.strptime(str(b['booking_time']), "%Y-%m-%d %H:%M:%S")
        b['status'] = "Expired" if (datetime.now() - booking_time).total_seconds() > 86400 else "Valid"

    return render_template('bookings.html', bookings=bookings)

@app.route('/ticket/<pnr>')
def ticket(pnr):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.pnr, s1.station_name AS source_name, s1.station_code AS source_code,
               s2.station_name AS destination_name, s2.station_code AS destination_code,
               b.booking_time, b.fare, b.qr_code_path, b.ticket_class, b.is_return,
               u.first_name, u.last_name
        FROM bookings b
        JOIN stations s1 ON b.source_station_id = s1.station_id
        JOIN stations s2 ON b.destination_station_id = s2.station_id
        JOIN users u ON b.user_id = u.id
        WHERE b.pnr = %s AND b.user_id = %s
    """, (pnr, session['user_id']))
    ticket = cursor.fetchone()
    cursor.close()
    conn.close()

    if not ticket:
        flash("Ticket not found", "danger")
        return redirect(url_for('bookings'))

    full_name = f"{ticket['first_name']} {ticket['last_name']}"
    return render_template('ticket.html', ticket=ticket, full_name=full_name)

if __name__ == '__main__':
    app.run(debug=True)