from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def build_sample_finance_dataset() -> dict[str, Any]:
    """Return a realistic quarterly close dataset for variance analysis."""
    gl_summary = [
        {
            "account": "Revenue",
            "category": "Operating Revenue",
            "amount": 8_725_000,
            "source_system": "Oracle ERP GL",
            "extraction_time": "2026-09-30T18:30:00Z",
            "version": "GL-2026Q3-09-30-v1",
        },
        {
            "account": "Payroll",
            "category": "Operating Expense",
            "amount": 3_450_000,
            "source_system": "Oracle ERP GL",
            "extraction_time": "2026-09-30T18:30:00Z",
            "version": "GL-2026Q3-09-30-v1",
        },
        {
            "account": "Marketing",
            "category": "Operating Expense",
            "amount": 680_000,
            "source_system": "Oracle ERP GL",
            "extraction_time": "2026-09-30T18:30:00Z",
            "version": "GL-2026Q3-09-30-v1",
        },
        {
            "account": "Trade Receivables",
            "category": "Balance Sheet",
            "amount": 1_240_000,
            "source_system": "Oracle ERP AR",
            "extraction_time": "2026-09-30T18:45:00Z",
            "version": "AR-2026Q3-09-30-v2",
        },
        {
            "account": "Trade Payables",
            "category": "Balance Sheet",
            "amount": 970_000,
            "source_system": "Oracle ERP AP",
            "extraction_time": "2026-09-30T18:47:00Z",
            "version": "AP-2026Q3-09-30-v2",
        },
    ]

    forecast = [
        {
            "account": "Revenue",
            "category": "Operating Revenue",
            "amount": 8_900_000,
            "source_system": "FP&A Forecast",
            "extraction_time": "2026-09-28T09:15:00Z",
            "version": "Forecast-2026Q3-v3",
        },
        {
            "account": "Payroll",
            "category": "Operating Expense",
            "amount": 3_300_000,
            "source_system": "FP&A Forecast",
            "extraction_time": "2026-09-28T09:15:00Z",
            "version": "Forecast-2026Q3-v3",
        },
        {
            "account": "Marketing",
            "category": "Operating Expense",
            "amount": 620_000,
            "source_system": "FP&A Forecast",
            "extraction_time": "2026-09-28T09:15:00Z",
            "version": "Forecast-2026Q3-v3",
        },
        {
            "account": "Trade Receivables",
            "category": "Balance Sheet",
            "amount": 1_350_000,
            "source_system": "FP&A Forecast",
            "extraction_time": "2026-09-28T09:15:00Z",
            "version": "Forecast-2026Q3-v3",
        },
        {
            "account": "Trade Payables",
            "category": "Balance Sheet",
            "amount": 915_000,
            "source_system": "FP&A Forecast",
            "extraction_time": "2026-09-28T09:15:00Z",
            "version": "Forecast-2026Q3-v3",
        },
    ]

    return {
        "reporting_period": "2026-Q3",
        "scenario": "Quarter-end variance review for operating and cash performance",
        "source_systems": [
            "Oracle ERP GL",
            "Oracle ERP AR",
            "Oracle ERP AP",
            "FP&A Forecast",
        ],
        "gl_summary": gl_summary,
        "forecast": forecast,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "controls": [
            "SOX-001: Source traceability validated",
            "SOX-002: Variance reason codes required",
            "SOX-003: Human approval checkpoint enforced",
        ],
    }
