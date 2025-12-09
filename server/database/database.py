import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv

current_path = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(current_path,"..","config",".env")
load_dotenv(dotenv_path=env_path)  # Load environment variables from .env file


DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")    


engine = create_engine(DATABASE_URL) # this line establishes actual connection pool to the database 


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Creates a new database session

Base = declarative_base()  # Base class from which all mapped classes should inherit 


def get_db():
    db = SessionLocal()
    try:
        yield db  #Gives the connection to the route that requested it  
    finally:
        db.close()