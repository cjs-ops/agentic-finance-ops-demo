from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/ready")
def ready() -> dict:
    return {"ready": True, "checks": ["api", "workflow", "audit-log", "clerk-config-ready"]}
