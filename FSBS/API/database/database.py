from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
load_dotenv()

# Create an SQLAlchemy engine that's connected to our postgres database
if os.getenv('FSBS_DB_URL') == None:
    raise Exception('Could not get database uri from environment variables. Consider setting JR_DB_URL in environment or adding it to a .env file.')


# Create an SQLAlchemy engine that's connected to our postgres database
engine = create_engine(url=os.getenv('FSBS_DB_URL'))

# database sessions will be created from the SessionLocal parent class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This base class is what we'll use to declare models
Base = declarative_base()