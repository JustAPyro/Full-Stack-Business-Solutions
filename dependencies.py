from structures.database import SessionLocal

# This is a database dependency
def database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
