from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    contact_info = Column(String, nullable=True)
    
    expenses = relationship("Expense", back_populates="supplier")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True) # e.g., 'Food', 'Drink', 'Ingredient'
    price = Column(Float) # Current selling price
    
    sales = relationship("Sale", back_populates="product")
    expenses = relationship("Expense", back_populates="product")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True) # If linked to a product
    name = Column(String) # Manual override or general name
    quantity = Column(Float)
    price = Column(Float)
    total_amount = Column(Float) # Auto-calculated
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    category = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="expenses")
    supplier = relationship("Supplier", back_populates="expenses")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_at_sale = Column(Float) # Recording price at time of sale
    total_amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="sales")

class CashOperationType(enum.Enum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"

class CashOperation(Base):
    __tablename__ = "cash_operations"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String) # 'INCOME' or 'OUTCOME'
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
