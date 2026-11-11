from sqlalchemy import create_engine, URL
## for loading credentials from .env file
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

# make postgresql connectoin url
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)

# sqlalchemy engine
engine = create_engine(connection_url)

# testing database connection
with engine.connect() as connection:
    print("Connection succesful")