from fastapi import APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel
from app.core.agent import agent_orchestrator
from app.models.user import User
from app.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class AgentRequest(BaseModel):
    prompt: str

@router.post("/process")
async def process_agent(request: AgentRequest, token: str = Header(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == int(token)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or deleted. Please log in again.")
    response = await agent_orchestrator(request.prompt)
    return response 