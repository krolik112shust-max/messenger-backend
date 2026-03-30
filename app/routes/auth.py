from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
import jwt
from datetime import datetime, timedelta
from app.config import settings

router = APIRouter()

class PhoneRequest(BaseModel):
    phone: str

class VerifyRequest(BaseModel):
    phone: str
    code: str

verification_codes = {}

def create_token(user_id: int):
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(days=30)}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

@router.post("/request-code")
async def request_code(req: PhoneRequest):
    verification_codes[req.phone] = "123456"
    return {"message": "Code sent", "code": "123456"}

@router.post("/verify-code")
async def verify_code(req: VerifyRequest, db: AsyncSession = Depends(get_db)):
    stored = verification_codes.get(req.phone)
    if not stored or stored != req.code:
        raise HTTPException(status_code=400, detail="Invalid code")
    
    result = await db.execute(select(User).where(User.phone == req.phone))
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(phone=req.phone, username=f"user_{req.phone[-4:]}")
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    token = create_token(user.id)
    del verification_codes[req.phone]
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}