from fastapi import APIRouter, HTTPException, status, Depends, Header
from pydantic import BaseModel, EmailStr
from app.models.user import User, UserCreate, UserRead
from app.core.auth import get_password_hash, verify_password
from app.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", response_model=UserRead)
def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_pw = get_password_hash(request.password)
    user = User(email=request.email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead(id=user.id, email=user.email)

@router.post("/login")
def login_user(request: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # For now, return user id as a simple session token
    return {"token": str(user.id), "user": {"id": user.id, "email": user.email}}

@router.delete("/admin/delete_all_users")
def delete_all_users(token: str = Header(...), db: Session = Depends(get_db)):
    # Only allow if token matches admin user
    admin = db.query(User).filter(User.email == "admin").first()
    if not admin or str(admin.id) != token:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.query(User).delete()
    db.commit()
    return {"message": "All users deleted."} 