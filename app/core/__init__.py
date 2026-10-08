from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.audit import AuditLogger
from app.workflows.finance_agent import run_finance_workflow

router = APIRouter(prefix="/finance", tags=["finance"])


class FinanceRequest(BaseModel):
    user: str = Field(default="analyst_001", description="User performing the review.")
    approval: bool = Field(default=True, description="Human approval checkpoint status.")
    gl_summary: list[dict[str, Any]] = Field(..., description="GL actuals with account references.")
    forecast: list[dict[str, Any]] = Field(..., description="Budget or forecast values.")


@router.post("/analyze-variance")
def analyze_variance(payload: FinanceRequest) -> dict[str, Any]:
    audit_logger = AuditLogger()
    audit_id = f"FIN-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

    result = run_finance_workflow(
        gl_summary=payload.gl_summary,
        forecast=payload.forecast,
        user=payload.user,
        approval_status=payload.approval,
    )

    audit_logger.log_event(
        source="finance-api",
        user=payload.user,
        action="variance-analysis-request",
        result="completed",
        control_mark="SOX-003",
        citation="finance-api:/finance/analyze-variance",
    )

    result["summary"]["audit_id"] = audit_id
    result["summary"]["generated_at"] = datetime.now(timezone.utc).isoformat()
    result["audit_id"] = audit_id

    return {
        "summary": result["summary"],
        "citations": result.get("citations", []),
        "control_checks": result.get("control_checks", []),
        "confidence": result.get("confidence", 0.0),
        "audit_id": audit_id,
    }


@router.get("/audit-trail")
def get_audit_trail() -> dict[str, Any]:
    logger = AuditLogger()
    return {"audit_trail": logger.get_trail()}
