from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy", "service": "ai-ops-mind", "version": "2.0.0"}
