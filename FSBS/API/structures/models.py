from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, JSON
from FSBS.API.database.database import Base


class User(Base):
    __tablename__ = 'users'
    # Track which users have which modules enabled

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


class APIRequest(Base):
    __tablename__ = 'api_requests'
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=False, nullable=True)
    endpoint = Column(String(255), unique=False, nullable=False)
    method = Column(String(255), unique=False, nullable=False)
    query = Column(String(255), unique=False, nullable=True)
    params = Column(JSONB, unique=False, nullable=True)
    body = Column(JSONB, unique=False, nullable=True)
    caller_ip = Column(String(255), unique=False, nullable=False)
    caller_port = Column(Integer, unique=False, nullable=False)
    time = Column(DateTime, unique=False, nullable=False)

# class History(Base):
#     __tablename__ = 'history'
#
#     history_id = Column(Integer, primary_key=True, autoincrement=True)
#
#     user_id = Column(Integer, ForeignKey('users.user_id'), unique=False, nullable=False)
#     user = relationship('User', back_populates='history')
#
#     method = Column(String(255), unique=False, nullable=False)
#     endpoint = Column(String(255), unique=False, nullable=False)
#
#
#     time = Column(DateTime, nullable=False)