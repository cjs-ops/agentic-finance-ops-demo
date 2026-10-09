from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from langgraph.graph import END, START, StateGraph

from app.agents.audit_agent import build_audit_summary
from app.agents.reconciliation_agent import reconcile_gl_to_forecast
from app.agents.variance_agent import analyze_variance
from app.core.audit import AuditLogger


class FinanceState(dict):
    pass


def extract_node(state: FinanceState) -> FinanceState:
    state["extracted"] = {
        "reporting_period": "2026-Q3",
        "scenario": "Quarter-end review for operating variance and cash-flow controls",
        "source_records": state.get("gl_summary", []) + state.get("forecast", []),
    }
    return state


def normalize_node(state: FinanceState) -> FinanceState:
    state["normalized"] = {
        "gl_summary": state.get("gl_summary", []),
        "forecast": state.get("forecast", []),
        "source_systems": sorted({item.get("source_system", "unknown") for item in state.get("gl_summary", []) + state.get("forecast", [])}),
    }
    return state


def reconcile_node(state: FinanceState) -> FinanceState:
    state["reconciliation"] = reconcile_gl_to_forecast(state.get("gl_summary", []), state.get("forecast", []))
    state["citations"] = state["reconciliation"].get("citations", [])
    return state


def variance_node(state: FinanceState) -> FinanceState:
    state["variance"] = analyze_variance(state.get("gl_summary", []), state.get("forecast", []))
    return state


def human_approval_node(state: FinanceState) -> FinanceState:
    approved = bool(state.get("approval_status", True))
    state["approval"] = {
        "approved": approved,
        "approver": state.get("user", "clerk-demo-user"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return state


def summary_node(state: FinanceState) -> FinanceState:
    reconciliation = state.get("reconciliation", {})
    variance = state.get("variance", {})
    citations = state.get("citations", [])
    audit_summary = build_audit_summary(reconciliation, variance, citations)

    approval = state.get("approval", {})
    summary_text = (
        f"{audit_summary['summary']} Approval status: {'approved' if approval.get('approved') else 'requires review'}."
    )

    state["summary"] = {
        "summary": summary_text,
        "status": "approved" if approval.get("approved") else "requires-review",
        "control_checks": audit_summary["control_checks"],
        "citations": citations,
        "confidence": variance.get("confidence", 0.0),
        "audit_id": f"FIN-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
    }

    logger = AuditLogger()
    logger.log_event(
        source="finance-workflow",
        user=state.get("user", "analyst_001"),
        action="final-summary",
        result=state["summary"]["status"],
        control_mark="SOX-003",
        citation="workflow:summary",
    )
    return state


def build_finance_workflow():
    workflow = StateGraph(FinanceState)
    workflow.add_node("extract", extract_node)
    workflow.add_node("normalize", normalize_node)
    workflow.add_node("reconcile", reconcile_node)
    workflow.add_node("variance", variance_node)
    workflow.add_node("approval", human_approval_node)
    workflow.add_node("summary", summary_node)

    workflow.set_entry_point("extract")
    workflow.add_edge("extract", "normalize")
    workflow.add_edge("normalize", "reconcile")
    workflow.add_edge("reconcile", "variance")
    workflow.add_edge("variance", "approval")
    workflow.add_edge("approval", "summary")
    workflow.add_edge("summary", END)

    return workflow.compile()


def run_finance_workflow(gl_summary: list[dict[str, Any]], forecast: list[dict[str, Any]], user: str = "analyst_001", approval_status: bool = True) -> dict[str, Any]:
    graph = build_finance_workflow()
    state: FinanceState = {
        "gl_summary": gl_summary,
        "forecast": forecast,
        "user": user,
        "approval_status": approval_status,
    }
    result = graph.invoke(state)
    return {
        "summary": result.get("summary", {}),
        "citations": result.get("citations", []),
        "control_checks": result.get("summary", {}).get("control_checks", []),
        "confidence": result.get("summary", {}).get("confidence", 0.0),
    }
