from flask import Flask, render_template
import psycopg

app = Flask(__name__)

# Csatlakozás a PostgreSQL adatbázishoz
conn = psycopg.connect(
    host="dpg-d100am3ipnbc738chka0-a.frankfurt-postgres.render.com",
    dbname="laciprojekt",
    user="laciprojekt_user",
    password="8izs5VoqaKrcOBjNYYTO3gXrvXAWnPKZ"
)

@app.route("/")
def index():
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, email FROM users")
        users = cur.fetchall()
    return render_template("index.html", users=users)
