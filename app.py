from flask import Flask, render_template, request, redirect
import psycopg
import os

app = Flask(__name__)

DB_URL = os.environ.get("DATABASE_URL")

@app.route('/')
def index():
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.id, u.name, a.date, a.time
                FROM appointments a
                JOIN users u ON a.user_id = u.id
                ORDER BY a.date, a.time
            """)
            bookings = cur.fetchall()
    return render_template('index.html', bookings=bookings)

@app.route('/foglalas', methods=['POST'])
def foglalas():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']

    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            # Ha nem létezik a user, létrehozzuk
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            if user:
                user_id = user[0]
            else:
                cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id", (name, email))
                user_id = cur.fetchone()[0]

            # Foglalás mentése
            cur.execute("INSERT INTO appointments (user_id, date, time) VALUES (%s, %s, %s)",
                        (user_id, date, time))
            conn.commit()
    return redirect('/')
