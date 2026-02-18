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

# Максимально разрешительный CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(data.router)
app.include_router(analytics.router)

@app.on_event("startup")
def startup_event():
    # Мы теперь создаем админа лениво в auth.py во время логина
    # Это предотвращает ошибки при запуске на некоторых платформах
    logger.info("Application starting up... Admin will be verified during login.")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Canteen Finance API is running"}
