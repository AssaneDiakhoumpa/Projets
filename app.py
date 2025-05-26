from flask import Flask, request
import psycopg2, datetime, timezone
app = Flask(__name__)
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="domotique",     
        user="azoupro",
        password=" "
    )
CREATE_salle_TABLE = (
    "CREATE TABLE IF NOT EXISTS salle (id SERIAL PRIMARY KEY, nom TEXT);"
)

INSERT_salle_RETURN_ID = "INSERT INTO salle (name) VALUES (%s) RETURNING id;"
@app.post("/api/salle")
def create_salle():
    data = request.get_json()
    nom = data["nom"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(CREATE_salle_TABLE)
    cur.execute(INSERT_salle_RETURN_ID)
    room_id = cur.fetchone()[0]
    return {"id": room_id, "message": f"salle {nom} creer."}, 201

CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL, 
                        date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""
INSERT_TEMP = (
    "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s, %s, %s);"
)
@app.post("/api/temperature")
def add_temp():
    data = request.get_json()
    temperature = data["temperature"]
    room_id = data["nom"]
    try:
        date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.now(timezone.utc)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(CREATE_TEMPS_TABLE)
    cur.execute(INSERT_TEMP, (room_id, temperature, date))
    return {"message": "Temperature added."}, 201

GLOBAL_NUMBER_OF_DAYS = (
    """SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures;"""
)
GLOBAL_AVG = """SELECT AVG(temperature) as average FROM temperatures;"""
@app.get("/api/moyenne")
def get_global_avg():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(GLOBAL_AVG)
    average = cur.fetchone()[0]
    cur.execute(GLOBAL_NUMBER_OF_DAYS)
    days = cur.fetchone()[0]
    return {"average": round(average, 2), "days": days}

if __name__ == "__main__":
	app.run(debug=True)