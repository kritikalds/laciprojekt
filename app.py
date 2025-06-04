from flask import Flask, render_template, redirect, url_for, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'valami-titkos-kulcs'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ADMIN user létrehozása
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

users = {
    'admin': User(1, 'admin', '$2b$12$Qq.S9xsNiZAwccLJk32VNOBDOPUgA.3SceinI9ASmujOLeSA/Aoee')
}

appointments = []  # ideiglenes lista az időpontokhoz

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == user_id:
            return user
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Hibás belépés', 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/idopontok', methods=['GET', 'POST'])
def idopontok():
    message = ''
    if request.method == 'POST':
        if current_user.is_authenticated:
            new_time = request.form['time']
            appointments.append(new_time)
            message = 'Sikeres foglalás.'
        else:
            message = 'Csak bejelentkezett felhasználók foglalhatnak időpontot.'
    return render_template('idopontok.html', appointments=appointments, message=message)

@app.route('/galeria')
def galeria():
    return '<h2>Galéria - Hamarosan!</h2>'

@app.route('/rolam')
def rolam():
    return '<h2>Rólam - Hamarosan!</h2>'

@app.route('/kapcsolat')
def kapcsolat():
    return '<h2>Kapcsolat - Hamarosan!</h2>'

if __name__ == '__main__':
    app.run(debug=True)
