from fastapi import FastAPI
from app.api import users, sessions, agent

app = FastAPI(title="Daedalus: Agentic Data Architect")

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(agent.router, prefix="/agent", tags=["agent"]) 