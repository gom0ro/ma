from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, data, analytics
from app.db.session import engine, Base

# Create tables (for production, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Canteen Finance Management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(data.router)
app.include_router(analytics.router)

from app.db.session import SessionLocal
from app.models.models import User
from app.core.security import get_password_hash

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin", 
            hashed_password=get_password_hash("admin123"), 
            full_name="System Admin"
        )
        db.add(admin)
        db.commit()
    db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Canteen Finance API"}
