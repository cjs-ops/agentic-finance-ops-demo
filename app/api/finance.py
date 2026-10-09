from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agents.audit_agent import build_audit_summary
from app.agents.reconciliation_agent import reconcile_gl_to_forecast
from app.agents.variance_agent import analyze_variance
from app.core.audit import AuditLogger

router = APIRouter(prefix="/finance", tags=["finance"])


class FinanceRequest(BaseModel):
    user: str = Field(default="analyst_001", description="User performing the review.")
    approval: bool = Field(default=True, description="Human approval checkpoint status.")
    gl_summary: list[dict[str, Any]] = Field(..., description="GL actuals.")
    forecast: list[dict[str, Any]] = Field(..., description="Forecast or budget records.")


@router.post("/analyze-variance")
def analyze_variance(payload: FinanceRequest) -> dict[str, Any]:
    logger = AuditLogger()
    audit_id = f"FIN-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

    reconciliation = reconcile_gl_to_forecast(payload.gl_summary, payload.forecast)
    variance = analyze_variance(payload.gl_summary, payload.forecast)
    citations = [
        {"source": row.get("source", "unknown"), "record": row.get("account", "unknown"), "version": "variance-review"}
        for row in reconciliation.get("variance_rows", [])
    ]

    if not payload.approval:
        raise HTTPException(status_code=400, detail="Human approval is required before final variance signoff.")

    audit_summary = build_audit_summary(reconciliation, variance, citations)
    logger.log_event(
        source="finance-api",
        user=payload.user,
        action="variance-analysis",
        result="completed",
        control_mark="SOX-003",
        citation="finance-api:/finance/analyze-variance",
    )

    response = {
        "summary": {
            "headline": audit_summary["summary"],
            "status": audit_summary["status"],
            "variance_total": variance["total_variance"],
            "key_findings": variance["key_findings"],
            "audit_id": audit_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "citations": citations,
        "control_checks": reconciliation["control_checks"] + audit_summary["control_checks"],
        "confidence": variance["confidence"],
        "audit_id": audit_id,
    }
    return response


@router.get("/audit-trail")
def get_audit_trail() -> dict[str, Any]:
    return {"audit_trail": AuditLogger().get_trail()}
