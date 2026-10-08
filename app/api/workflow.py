from fastapi import APIRouter

router = APIRouter(prefix="/workflow", tags=["workflow"])

@router.get("/status")
def workflow_status():
    return {
        "status": "ready",
        "workflow": "finance-variance-and-reconciliation",
        "steps": [
            "extract",
            "normalize",
            "reconcile",
            "variance-analysis",
            "human-approval",
            "final-summary"
        ]
    }
