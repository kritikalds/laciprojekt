from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# PostgreSQL csatlakozás
conn = psycopg2.connect(
    host="dpg-d100am3ipnbc738chka0-a.frankfurt-postgres.render.com",
    port=5432,
    database="laciprojekt",
    user="laciprojekt_user",
    password="8izs5VoqaKrcOBjNYYTO3gXrvXAWnPKZ"
)

@app.route("/foglalas", methods=["POST"])
def foglalas():
    data = request.json
    nev = data.get("nev")
    datum = data.get("datum")
    ora = data.get("ora")

    cur = conn.cursor()
    cur.execute("INSERT INTO idopontok (nev, datum, ora) VALUES (%s, %s, %s)", (nev, datum, ora))
    conn.commit()
    cur.close()

    return jsonify({"status": "sikeres foglalas"})

@app.route("/idopontok", methods=["GET"])
def get_idopontok():
    cur = conn.cursor()
    cur.execute("SELECT nev, datum, ora FROM idopontok ORDER BY datum, ora")
    rows = cur.fetchall()
    cur.close()

    return jsonify([
        {"nev": r[0], "datum": str(r[1]), "ora": str(r[2])}
        for r in rows
    ])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
