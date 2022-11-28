from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an SQLAlchemy engine that's connected to our postgres database
engine = create_engine(url='postgresql://postgres:postgreSQLpassword@localhost/fsbs_development')

# database sessions will be created from the SessionLocal parent class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This base class is what we'll use to declare models
Base = declarative_base()