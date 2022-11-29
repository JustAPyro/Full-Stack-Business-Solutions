from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from FSBS.API.database.database import Base


class User(Base):
    __tablename__ = 'users'

    # Primary key user ID and email which acts as username
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)

    # Password field
    password = Column(String(255), unique=False, nullable=False)

    # User information
    first_name = Column(String(255), unique=False, nullable=False)
    last_name = Column(String(255), unique=False, nullable=False)
    phone = Column(String(255), unique=True, nullable=True)

    # Activity information
    date_registered = Column(DateTime, nullable=False)
    date_last_active = Column(DateTime, nullable=False)

    purchases = relationship("Purchase", back_populates="user")


class Purchase(Base):
    __tablename__ = 'purchases'

    # The transaction_id and the user_id of the owner
    purchase_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('users.user_id'), unique=False, nullable=False)
    user = relationship('User', back_populates='purchases')

    # Store the location of the transaction
    location = Column(String(255), unique=False, nullable=False)

    # Store the cost and tax of the transaction
    cost = Column(Integer, unique=False, nullable=False)
    tax = Column(Integer, unique=False, nullable=False)

    # Save the time of the purchase
    purchase_time = Column(DateTime, nullable=False)
