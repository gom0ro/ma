from app.db.session import SessionLocal, engine, Base
from app.models.models import User, Product, Supplier, Expense, Sale, CashOperation
from app.core.security import get_password_hash
from datetime import datetime
import random

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Create admin
    admin = User(username="admin", hashed_password=get_password_hash("admin123"), full_name="System Admin")
    db.add(admin)
    db.commit()
    db.close()
    print("Database cleared! Admin user 'admin'/'admin123' created.")

if __name__ == "__main__":
    seed()
