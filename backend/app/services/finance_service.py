from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from app.models.models import Sale, Expense, CashOperation, Product, Supplier
from datetime import datetime, date, timedelta
import pandas as pd

class FinanceService:
    @staticmethod
    def get_daily_stats(db: Session, target_date: date):
        # Revenue from sales
        revenue = db.query(func.sum(Sale.total_amount)).filter(
            func.date(Sale.date) == target_date
        ).scalar() or 0.0
        
        # Expenses
        expenses = db.query(func.sum(Expense.total_amount)).filter(
            func.date(Expense.date) == target_date
        ).scalar() or 0.0
        
        # Profit
        profit = revenue - expenses
        
        # Sold count
        sold_count = db.query(func.sum(Sale.quantity)).filter(
            func.date(Sale.date) == target_date
        ).scalar() or 0
        
        # Top 5 products
        top_products_query = db.query(
            Product.name, func.sum(Sale.quantity).label('total_qty')
        ).join(Sale).filter(
            func.date(Sale.date) == target_date
        ).group_by(Product.id).order_by(func.sum(Sale.quantity).desc()).limit(5).all()
        
        top_products = [{"name": r[0], "value": r[1]} for r in top_products_query]
        
        # Chart data (last 7 days)
        chart_labels = []
        chart_revenue = []
        for i in range(6, -1, -1):
            d = target_date - timedelta(days=i)
            rev = db.query(func.sum(Sale.total_amount)).filter(
                func.date(Sale.date) == d
            ).scalar() or 0.0
            chart_labels.append(d.strftime("%Y-%m-%d"))
            chart_revenue.append(rev)
            
        # Expenses by category
        exp_categories = db.query(
            Expense.category, func.sum(Expense.total_amount)
        ).filter(
            func.date(Expense.date) == target_date
        ).group_by(Expense.category).all()
        
        expense_chart = {
            "labels": [r[0] for r in exp_categories],
            "data": [r[1] for r in exp_categories]
        }

        return {
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit,
            "sold_count": sold_count,
            "top_products": top_products,
            "line_chart": {"labels": chart_labels, "data": chart_revenue},
            "pie_chart": expense_chart
        }

    @staticmethod
    def get_comparison(db: Session, date1: date, date2: date):
        def get_totals(d):
            rev = db.query(func.sum(Sale.total_amount)).filter(func.date(Sale.date) == d).scalar() or 0.0
            exp = db.query(func.sum(Expense.total_amount)).filter(func.date(Expense.date) == d).scalar() or 0.0
            return rev, exp

        rev1, exp1 = get_totals(date1)
        rev2, exp2 = get_totals(date2)
        
        prof1 = rev1 - exp1
        prof2 = rev2 - exp2
        
        def calc_diff(v1, v2):
            if v1 == 0: return 100 if v2 > 0 else 0
            return round(((v2 - v1) / v1) * 100, 2)

        return {
            "date1": date1.isoformat(),
            "date2": date2.isoformat(),
            "revenue": {"val1": rev1, "val2": rev2, "diff": calc_diff(rev1, rev2)},
            "expenses": {"val1": exp1, "val2": exp2, "diff": calc_diff(exp1, exp2)},
            "profit": {"val1": prof1, "val2": prof2, "diff": calc_diff(prof1, prof2)},
            "suppliers1": db.query(Supplier.name, func.sum(Expense.total_amount)).join(Expense).filter(func.date(Expense.date) == date1).group_by(Supplier.id).all(),
            "suppliers2": db.query(Supplier.name, func.sum(Expense.total_amount)).join(Expense).filter(func.date(Expense.date) == date2).group_by(Supplier.id).all()
        }
        
    @staticmethod
    def get_monthly_stats(db: Session):
        today = date.today()
        first_day = today.replace(day=1)
        
        revenue = db.query(func.sum(Sale.total_amount)).filter(
            func.date(Sale.date) >= first_day
        ).scalar() or 0.0
        
        expenses = db.query(func.sum(Expense.total_amount)).filter(
            func.date(Expense.date) >= first_day
        ).scalar() or 0.0
        
        profit = revenue - expenses
        margin = round((profit / revenue * 100), 2) if revenue > 0 else 0
        
        # Monthly trend
        labels = []
        rev_data = []
        exp_data = []
        for i in range(5, -1, -1):
            target_month = (datetime.now() - timedelta(days=i*30)).replace(day=1)
            month_label = target_month.strftime("%b")
            
            m_rev = db.query(func.sum(Sale.total_amount)).filter(
                extract('month', Sale.date) == target_month.month,
                extract('year', Sale.date) == target_month.year
            ).scalar() or 0.0
            
            m_exp = db.query(func.sum(Expense.total_amount)).filter(
                extract('month', Expense.date) == target_month.month,
                extract('year', Expense.date) == target_month.year
            ).scalar() or 0.0
            
            labels.append(month_label)
            rev_data.append(m_rev)
            exp_data.append(m_exp)
            
        return {
            "monthly_revenue": revenue,
            "monthly_expenses": expenses,
            "profit_margin": margin,
            "chart": {
                "labels": labels,
                "revenue": rev_data,
                "expenses": exp_data
            }
        }
        total_income = db.query(func.sum(CashOperation.amount)).filter(CashOperation.type == 'INCOME').scalar() or 0.0
        total_outcome = db.query(func.sum(CashOperation.amount)).filter(CashOperation.type == 'OUTCOME').scalar() or 0.0
        
        # Purchases (Expenses) are also outcomes
        total_purchases = db.query(func.sum(Expense.total_amount)).scalar() or 0.0
        
        # Revenue from sales are also incomes
        total_sales = db.query(func.sum(Sale.total_amount)).scalar() or 0.0
        
        balance = (total_income + total_sales) - (total_outcome + total_purchases)
        
        return {
            "balance": balance,
            "total_purchases": total_purchases,
            "total_sales": total_sales,
            "remaining": balance
        }
