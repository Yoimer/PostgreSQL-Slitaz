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
    flights = db.execute("SELECT origin, destination, duration FROM flights").fetchall()
    for flight in flights:
        print(f"{flight.origin} to {flight.destination}, {flight.duration} minutes.")
        # print(flight)
        
if __name__ == "__main__":
    main()
