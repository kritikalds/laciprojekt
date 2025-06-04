from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

import os

app = Flask(__name__)
app.secret_key = 'supertitkoskulcs'  # titkos kulcs session-höz

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin_login"

DB_URL = os.environ.get("DATABASE_URL")


# Admin user osztály flask-loginhez
class AdminUser(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(admin_id):
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username FROM admins WHERE id = %s", (admin_id,))
            admin = cur.fetchone()
            if admin:
                return AdminUser(admin[0], admin[1])
    return None


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, password_hash FROM admins WHERE username = %s", (username,))
                admin = cur.fetchone()
                if admin and bcrypt.check_password_hash(admin[1], password):
                    user = AdminUser(admin[0], username)
                    login_user(user)
                    return redirect(url_for('admin_panel'))
                else:
                    flash("Hibás felhasználónév vagy jelszó", "danger")

    return render_template('admin_login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))


@app.route('/admin')
@login_required
def admin_panel():
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.id, u.name, u.email, a.date, a.time 
                FROM appointments a
                JOIN users u ON a.user_id = u.id
                ORDER BY a.date, a.time
            """)
            bookings = cur.fetchall()
    return render_template('admin_panel.html', bookings=bookings)


@app.route('/admin/delete/<int:booking_id>', methods=['POST'])
@login_required
def admin_delete_booking(booking_id):
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM appointments WHERE id = %s", (booking_id,))
            conn.commit()
    flash("Foglalás törölve", "success")
    return redirect(url_for('admin_panel'))
