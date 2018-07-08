import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

'''
engine = create_engine(os.getenv("DATABASE_URL"))
this line has to be replaced.
user has to create a database, a role and a password as shown above
where:
user: cs50
password: 12345
databasename : c50example
port: 5432 (default port)
'''

engine = create_engine("postgresql://cs50:12345@localhost:5432/cs50example")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():

    # Get all of the flights in the database, send them to our index.html template.
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""

    # Get form information.
    name = request.form.get("name")

    # Make sure that the flight id is a number (in case of a weird error).
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")

    # Make sure the flight exists.
    if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
        return render_template("error.html", message="No such flight with that id.")

    # If the flight exists, record the passenger as having registered for the flight.
    db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
            {"name": name, "flight_id": flight_id})

    # All done booking!
    db.commit()
    return render_template("success.html")
