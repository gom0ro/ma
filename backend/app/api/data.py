from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.session import get_db
from app.services.crud_service import CRUDService
from app.schemas.schemas import (
    SupplierSchema, SupplierCreate, 
    ProductSchema, ProductCreate, 
    ExpenseSchema, ExpenseCreate, 
    SaleSchema, SaleCreate,
    CashOperationSchema, CashOperationCreate
)
from app.api.auth import get_current_user

router = APIRouter(prefix="/data", tags=["data"], dependencies=[Depends(get_current_user)])

# Suppliers
@router.get("/suppliers", response_model=List[SupplierSchema])
def get_suppliers(db: Session = Depends(get_db)):
    return CRUDService.get_suppliers(db)

@router.post("/suppliers", response_model=SupplierSchema)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    return CRUDService.create_supplier(db, supplier)

@router.delete("/suppliers/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    success = CRUDService.delete_supplier(db, supplier_id)
    if not success:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"message": "Supplier deleted"}

# Products
@router.get("/products", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    return CRUDService.get_products(db)

@router.post("/products", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return CRUDService.create_product(db, product)

# Expenses
@router.get("/expenses", response_model=List[ExpenseSchema])
def get_expenses(
    supplier_id: Optional[int] = None, 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    db: Session = Depends(get_db)
):
    return CRUDService.get_expenses(db, supplier_id, start_date, end_date)

@router.post("/expenses", response_model=ExpenseSchema)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return CRUDService.create_expense(db, expense)

# Sales
@router.post("/sales", response_model=SaleSchema)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    res = CRUDService.create_sale(db, sale)
    if not res:
        raise HTTPException(status_code=404, detail="Product not found")
    return res

# Cash
@router.get("/cash/history", response_model=List[CashOperationSchema])
def get_cash_history(db: Session = Depends(get_db)):
    return CRUDService.get_cash_history(db)

@router.post("/cash", response_model=CashOperationSchema)
def create_cash_op(op: CashOperationCreate, db: Session = Depends(get_db)):
    return CRUDService.create_cash_operation(db, op)
