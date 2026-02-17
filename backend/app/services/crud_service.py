from sqlalchemy.orm import Session
from app.models.models import User, Supplier, Product, Expense, Sale, CashOperation
from app.schemas.schemas import UserCreate, SupplierCreate, ProductCreate, ExpenseCreate, SaleCreate, CashOperationCreate
from app.core.security import get_password_hash

class CRUDService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        db_user = User(username=user.username, hashed_password=get_password_hash(user.password), full_name=user.full_name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_suppliers(db: Session):
        return db.query(Supplier).all()

    @staticmethod
    def create_supplier(db: Session, supplier: SupplierCreate):
        db_obj = Supplier(**supplier.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_products(db: Session):
        return db.query(Product).all()

    @staticmethod
    def create_product(db: Session, product: ProductCreate):
        db_obj = Product(**product.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_expenses(db: Session, supplier_id: int = None, start_date: str = None, end_date: str = None):
        query = db.query(Expense)
        if supplier_id:
            query = query.filter(Expense.supplier_id == supplier_id)
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        return query.all()

    @staticmethod
    def create_expense(db: Session, expense: ExpenseCreate):
        total = expense.quantity * expense.price
        db_obj = Expense(**expense.model_dump(), total_amount=total)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def create_sale(db: Session, sale: SaleCreate):
        product = db.query(Product).filter(Product.id == sale.product_id).first()
        if not product:
            return None
        total = sale.quantity * product.price
        db_obj = Sale(**sale.model_dump(), price_at_sale=product.price, total_amount=total)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_cash_history(db: Session):
        return db.query(CashOperation).order_by(CashOperation.date.desc()).all()

    @staticmethod
    def create_cash_operation(db: Session, op: CashOperationCreate):
        db_obj = CashOperation(**op.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
