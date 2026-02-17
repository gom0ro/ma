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

@app.get("/")
def read_root():
    return {"message": "Welcome to Canteen Finance API"}
