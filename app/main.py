from fastapi import FastAPI

from app.api.finance import router as finance_router
from app.api.health import router as health_router
from app.api.workflow import router as workflow_router

app = FastAPI(
    title="Agentic Finance Ops Demo",
    description="Audit-aware multi-agent workflow for variance analysis, reconciliation, and close review.",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(workflow_router)
app.include_router(finance_router)


@app.get("/")
def root() -> dict:
    return {
        "service": "agentic-finance-ops-demo",
        "status": "ok",
        "workflow": "finance-variance-and-reconciliation",
        "auditable": True,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
