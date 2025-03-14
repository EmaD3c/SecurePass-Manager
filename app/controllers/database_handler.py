from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Connect to the database
engine = create_engine("postgresql://postgres:postgres@db:5432/postgres")

# Create a connection
connection = engine.connect()

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
db_session = Session()
