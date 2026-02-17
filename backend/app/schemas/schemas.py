from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Supplier Schemas
class SupplierBase(BaseModel):
    name: str
    contact_info: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierSchema(SupplierBase):
    id: int
    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    name: str
    category: str
    price: float

class ProductCreate(ProductBase):
    pass

class ProductSchema(ProductBase):
    id: int
    class Config:
        from_attributes = True

# Expense Schemas
class ExpenseBase(BaseModel):
    name: str
    quantity: float
    price: float
    supplier_id: int
    category: str
    product_id: Optional[int] = None
    date: datetime = Field(default_factory=datetime.utcnow)

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseSchema(ExpenseBase):
    id: int
    total_amount: float
    supplier: SupplierSchema
    class Config:
        from_attributes = True

# Sale Schemas
class SaleBase(BaseModel):
    product_id: int
    quantity: int
    date: datetime = Field(default_factory=datetime.utcnow)

class SaleCreate(SaleBase):
    pass

class SaleSchema(SaleBase):
    id: int
    price_at_sale: float
    total_amount: float
    product: ProductSchema
    class Config:
        from_attributes = True

# Cash Operation Schemas
class CashOperationBase(BaseModel):
    amount: float
    type: str # 'INCOME' or 'OUTCOME'
    description: str
    date: datetime = Field(default_factory=datetime.utcnow)

class CashOperationCreate(CashOperationBase):
    pass

class CashOperationSchema(CashOperationBase):
    id: int
    class Config:
        from_attributes = True

# Analytics Schemas
class DailyStats(BaseModel):
    revenue: float
    expenses: float
    profit: float
    sold_count: int
    top_products: List[dict]
    chart_data: dict

class ComparisonResult(BaseModel):
    date1: str
    date2: str
    revenue: dict # {'val1': x, 'val2': y, 'diff_pct': z}
    expenses: dict
    profit: dict
    suppliers: List[dict]
