from app.core.security import create_access_token
from app.api.auth import get_current_user
from app.db.session import SessionLocal
from jose import jwt
from app.core.config import settings
import datetime

token = create_access_token({"sub": "admin"})
print(f"Generated token: {token}")

try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print(f"Decoded payload: {payload}")
except Exception as e:
    print(f"Error decoding: {e}")

db = SessionLocal()
try:
    from app.models.models import User
    user = db.query(User).filter(User.username == "admin").first()
    print(f"User in DB: {user.username if user else 'Not found'}")
finally:
    db.close()
