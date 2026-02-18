from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import Optional

from app.db.session import get_db
from app.services.finance_service import FinanceService
from app.api.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"], dependencies=[Depends(get_current_user)])

@router.get("/daily")
def get_daily_stats(target_date: Optional[date] = None, db: Session = Depends(get_db)):
    if not target_date:
        target_date = date.today()
    return FinanceService.get_daily_stats(db, target_date)

@router.get("/monthly")
def get_monthly_stats(db: Session = Depends(get_db)):
    return FinanceService.get_monthly_stats(db)

@router.get("/compare")
def compare_dates(date1: date, date2: date, db: Session = Depends(get_db)):
    return FinanceService.get_comparison(db, date1, date2)

@router.get("/cash-summary")
def get_cash_summary(db: Session = Depends(get_db)):
    return FinanceService.get_cash_summary(db)

@router.get("/calendar-summary")
def get_calendar_summary(year: int, month: int, db: Session = Depends(get_db)):
    return FinanceService.get_calendar_stats(db, year, month)
