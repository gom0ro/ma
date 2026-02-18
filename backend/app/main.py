from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, data, analytics
from app.db.session import engine, Base, SessionLocal
from app.models.models import User
from app.core.security import get_password_hash
import logging

# Настройка логов для отладки в Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем таблицы
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

app = FastAPI(title="Canteen Finance Management")

# Максимально разрешительный CORS для GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gom0ro.github.io",
        "http://localhost:3000",
        "http://localhost:5173",
        "*"
    ],
    allow_credentials=False, # Ставим False, чтобы разрешить "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(data.router)
app.include_router(analytics.router)

@app.on_event("startup")
def startup_event():
    try:
        db = SessionLocal()
        admin = db.query(User).filter(User.username == "admin").first()
        hashed_pw = get_password_hash("admin123")
        
        if not admin:
            admin = User(
                username="admin", 
                hashed_password=hashed_pw, 
                full_name="System Admin"
            )
            db.add(admin)
            db.commit()
            logger.info("Default admin user created with password 'admin123'")
        else:
            # Принудительно обновляем пароль, если он вдруг не совпадает (напр. после смены хеширования)
            admin.hashed_password = hashed_pw
            db.commit()
            logger.info("Admin password reset to 'admin123'")
            
        db.close()
    except Exception as e:
        logger.error(f"Startup error: {e}")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Canteen Finance API is running"}
