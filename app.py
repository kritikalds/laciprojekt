from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'Qx8E@v!P1kZ#bTfL$3YrMn2s^dL0cVu7'

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

# PostgreSQL kapcsolat
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)
cursor = conn.cursor()

@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (int(user_id),))
    user = cursor.fetchone()
    if user:
        return User(*user)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and bcrypt.check_password_hash(user[3], password):
            user_obj = User(user[0], user[1], user[2])
            login_user(user_obj)
            return redirect(url_for('idopontok'))
        return render_template('login.html', error="Hibás bejelentkezés")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/idopontok', methods=['GET', 'POST'])
@login_required
def idopontok():
    if request.method == 'POST':
        datum = request.form['datum']
        leiras = request.form['leiras']
        cursor.execute("INSERT INTO appointments (user_id, datum, leiras) VALUES (%s, %s, %s)", (current_user.id, datum, leiras))
        conn.commit()
        return render_template('idopontok.html', success=True)

    if current_user.email == 'admin@example.com':
        cursor.execute("SELECT a.id, u.name, a.datum, a.leiras FROM appointments a JOIN users u ON a.user_id = u.id ORDER BY datum")
        appointments = cursor.fetchall()
        return render_template('idopontok.html', appointments=appointments)
    else:
        return render_template('idopontok.html')

if __name__ == '__main__':
    app.run(debug=True)
