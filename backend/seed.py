from app.db.session import SessionLocal, engine, Base
from app.models.models import User, Product, Supplier, Expense, Sale, CashOperation
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random
import sys

def seed(fill=False):
    if not fill:
        confirm = input("WARNING: This will DELETE all existing data! Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # 1. Create admin
    admin = User(username="admin", hashed_password=get_password_hash("admin123"), full_name="System Admin")
    db.add(admin)
    
    if fill:
        print("Filling with demo data...")
        # 2. Suppliers
        suppliers = [
            Supplier(name="FoodExpress", contact_info="+77010001122"),
            Supplier(name="DrinkMaster", contact_info="+77029998877"),
            Supplier(name="EcoFarm", contact_info="+77055554433")
        ]
        db.add_all(suppliers)
        db.commit()

        # 3. Products
        products = [
            Product(name="Кофе Капучино", category="Напитки", price=850),
            Product(name="Чай Зеленый", category="Напитки", price=400),
            Product(name="Бургер Классик", category="Еда", price=1200),
            Product(name="Салат Цезарь", category="Еда", price=1500),
            Product(name="Булочка с корицей", category="Выпечка", price=350)
        ]
        db.add_all(products)
        db.commit()

        # 4. Generate Sales and Expenses for the last 7 days
        today = datetime.now()
        for i in range(7):
            d = today - timedelta(days=i)
            
            # 5-10 random sales per day
            for _ in range(random.randint(5, 12)):
                prod = random.choice(products)
                qty = random.randint(1, 3)
                sale = Sale(
                    product_id=prod.id,
                    quantity=qty,
                    price_at_sale=prod.price,
                    total_amount=qty * prod.price,
                    date=d - timedelta(hours=random.randint(1, 8))
                )
                db.add(sale)

            # 1-2 random expenses per day
            for _ in range(random.randint(1, 2)):
                supp = random.choice(suppliers)
                price = random.randint(2000, 8000)
                qty = random.randint(1, 5)
                exp = Expense(
                    name=f"Закупка продуктов ({supp.name})",
                    quantity=qty,
                    price=price,
                    total_amount=qty * price,
                    supplier_id=supp.id,
                    category=random.choice(["Продукты", "Хоз.товары", "Прочее"]),
                    date=d - timedelta(hours=random.randint(1, 10))
                )
                db.add(exp)
        
        db.commit()
        print("Demo data created successfully!")

    db.commit()
    db.close()
    print("Database ready! Admin: 'admin' / 'admin123'")

if __name__ == "__main__":
    fill_data = "--fill" in sys.argv
    seed(fill=fill_data)
