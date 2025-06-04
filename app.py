from flask import Flask, request, redirect, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'valami-titkos-kulcs'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# Az admin user definíciója
users = {
    'admin': User(1, 'admin', '$2b$12$Qq.S9xsNiZAwccLJk32VNOBDOPUgA.3SceinI9ASmujOLeSA/Aoee')  # ide a hash-t tedd be!
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == user_id:
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect('/admin')
        else:
            return 'Hibás felhasználónév vagy jelszó', 401
    return '''
        <form method="post">
            Felhasználónév: <input name="username"><br>
            Jelszó: <input name="password" type="password"><br>
            <input type="submit" value="Bejelentkezés">
        </form>
    '''

@app.route('/admin')
@login_required
def admin():
    return f'Üdv, {current_user.username}! Itt tudsz időpontokat kezelni.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Kijelentkeztél.'

if __name__ == '__main__':
    app.run(debug=True)
