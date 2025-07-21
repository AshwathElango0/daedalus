from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
from app.models.user import Base, User
from app.core.auth import get_password_hash

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Automatic DB Initialization ---
def init_db():
    inspector = inspect(engine)
    if not inspector.has_table("users"):
        Base.metadata.create_all(bind=engine)
        # Add default admin user
        db = SessionLocal()
        try:
            admin = User(email="admin", hashed_password=get_password_hash("admin"))
            db.add(admin)
            db.commit()
        finally:
            db.close()

init_db() 