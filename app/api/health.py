from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/ready")
def ready():
    return {"ready": True, "checks": ["api", "workflow", "audit-log"]}
