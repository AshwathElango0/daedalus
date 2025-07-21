from fastapi import APIRouter

router = APIRouter()

@router.get("/check")
def check_session():
    # TODO: Implement session check logic
    return {"status": "ok"}

@router.post("/logout")
def logout():
    # TODO: Implement logout logic
    return {"message": "Logged out"} 