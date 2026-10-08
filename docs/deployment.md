from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, TypedDict

from app.agents.audit_agent import build_audit_summary
from app.agents.reconciliation_agent import reconcile_gl_to_forecast
from app.agents.variance_agent import analyze_variance
from app.core.audit import AuditLogger

try:
    from langgraph.graph import END, StateGraph
    LANGGRAPH_AVAILABLE = True
except ImportError:  # pragma: no cover
    LANGGRAPH_AVAILABLE = False
    END = "__end__"

    class StateGraph:  # type: ignore[override]
        def __init__(self, *args, **kwargs):
            raise RuntimeError("langgraph is required. Install the project requirements first.")


class FinanceState(TypedDict, total=False):
    gl_summary: list[dict[str, Any]]
    forecast: list[dict[str, Any]]
    user: str
    approval_status: bool
    extracted: dict[str, Any]
    normalized: dict[str, Any]
    reconciliation: dict[str, Any]
    variance: dict[str, Any]
    approval: dict[str, Any]
    summary: dict[str, Any]
    citations: list[dict[str, Any]]
    control_checks: list[dict[str, Any]]
    confidence: float


def _extract_data(state: FinanceState) -> dict[str, Any]:
    extracted = {
        "reporting_period": "2026-Q3",
        "scenario": "Quarter-end review for operating variance and cash-flow controls",
        "source_records": state.get("gl_summary", []) + state.get("forecast", []),
    }
    return {"extracted": extracted}


def _normalize_data(state: FinanceState) -> dict[str, Any]:
    normalized = {
        "gl_summary": state.get("gl_summary", []),
        "forecast": state.get("forecast", []),
        "source_systems": sorted({item.get("source_system", "unknown") for item in state.get("gl_summary", []) + state.get("forecast", [])}),
    }
    return {"normalized": normalized}


def _reconcile_accounts(state: FinanceState) -> dict[str, Any]:
    reconciliation = reconcile_gl_to_forecast(state.get("gl_summary", []), state.get("forecast", []))
    citations = [
        {"source": item.get("source", "ERP-GL"), "record": item.get("record", "unknown"), "version": item.get("version", "v1")}
        for item in reconciliation.get("citations", [])
    ]
    return {"reconciliation": reconciliation, "citations": citations}


def _variance_check(state: FinanceState) -> dict[str, Any]:
    variance = analyze_variance(state.get("gl_summary", []), state.get("forecast", []))
    return {"variance": variance}


def _human_approval(state: FinanceState) -> dict[str, Any]:
    approved = state.get("approval_status", True)
    approval = {
        "approved": bool(approved),
        "approver": state.get("user", "clerk-demo-user"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checkpoint": "SOX-003: Human approval checkpoint",
    }
    return {"approval": approval}


def _summarize(state: FinanceState) -> dict[str, Any]:
    reconciliation = state.get("reconciliation", {})
    variance = state.get("variance", {})
    citations = state.get("citations", [])
    audit_summary = build_audit_summary(reconciliation, variance, citations)

    key_findings = variance.get("key_findings", [])
    total_variance = variance.get("total_variance", 0)
    narrative = (
        f"Variance review complete. {', '.join(key_findings[:2]) if key_findings else 'No major variance outside tolerance.'} "
        f"Total variance is ${total_variance:,.0f}."
    )

    summary = {
        "summary": narrative,
        "reporting_period": state.get("normalized", {}).get("source_systems", ["2026-Q3"])[0] if state.get("normalized", {}).get("source_systems") else "2026-Q3",
        "status": "approved" if state.get("approval", {}).get("approved") else "requires-review",
        "control_checks": audit_summary["control_checks"],
        "citations": citations,
        "confidence": variance.get("confidence", 0.0),
    }

    logger = AuditLogger()
    logger.log_event(
        source="finance-workflow",
        user=state.get("user", "analyst_001"),
        action="final-summary-generated",
        result="completed",
        control_mark="SOX-003",
        citation="workflow:summary",
    )

    return {"summary": summary, "control_checks": audit_summary["control_checks"], "confidence": variance.get("confidence", 0.0)}


def build_finance_workflow():
    if not LANGGRAPH_AVAILABLE:
        raise RuntimeError("langgraph is required. Please install dependencies with pip install -r requirements.txt.")

    workflow = StateGraph(FinanceState)
    workflow.add_node("extract_data", _extract_data)
    workflow.add_node("normalize_data", _normalize_data)
    workflow.add_node("reconcile_accounts", _reconcile_accounts)
    workflow.add_node("variance_check", _variance_check)
    workflow.add_node("human_approval", _human_approval)
    workflow.add_node("summarize", _summarize)

    workflow.set_entry_point("extract_data")
    workflow.add_edge("extract_data", "normalize_data")
    workflow.add_edge("normalize_data", "reconcile_accounts")
    workflow.add_edge("reconcile_accounts", "variance_check")
    workflow.add_edge("variance_check", "human_approval")
    workflow.add_edge("human_approval", "summarize")
    workflow.add_edge("summarize", END)

    return workflow.compile()


def run_finance_workflow(gl_summary: list[dict[str, Any]], forecast: list[dict[str, Any]], user: str = "analyst_001", approval_status: bool = True) -> dict[str, Any]:
    graph = build_finance_workflow()
    initial_state: FinanceState = {
        "gl_summary": gl_summary,
        "forecast": forecast,
        "user": user,
        "approval_status": approval_status,
    }
    result = graph.invoke(initial_state)

    logger = AuditLogger()
    logger.log_event(
        source="finance-workflow",
        user=user,
        action="workflow-executed",
        result="success",
        control_mark="SOX-001",
        citation="workflow:run_finance_workflow",
    )

    return {
        "summary": result.get("summary", {"summary": "No output produced."}),
        "citations": result.get("citations", []),
        "control_checks": result.get("control_checks", []),
        "confidence": result.get("confidence", 0.0),
        "audit_trail": logger.get_trail(),
    }
