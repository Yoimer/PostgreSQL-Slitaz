import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

def main():

    # List all flights.
    flights = db.execute("SELECT id, origin, destination, duration FROM flights").fetchall()
    for flight in flights:
        print(f"Flight {flight.id}: {flight.origin} to {flight.destination}, {flight.duration} minutes.")

    # Prompt user to choose a flight.
    flight_id = int(input("\nFlight ID: "))
    flight = db.execute("SELECT origin, destination, duration FROM flights WHERE id = :id",
                        {"id": flight_id}).fetchone()

    # Make sure flight is valid.
    if flight is None:
        print("Error: No such flight.")
        return

    # List passengers.
    passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                            {"flight_id": flight_id}).fetchall()
    print("\nPassengers:")
    for passenger in passengers:
        print(passenger.name)
    if len(passengers) == 0:
        print("No passengers.")

if __name__ == "__main__":
    main()
