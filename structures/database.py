import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load the environment variables that might relate to DB
from dotenv import load_dotenv
load_dotenv()

# Get the database URL
url = os.getenv('FSBS_DB_URL')

# Verify the URL is valid
if url == None: raise Exception('Could not get database URI from enviornment variables. Please set FSBS_DB_URL.')

# Create a database engine and a session maker device
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class to declare database models from
Base = declarative_base()

