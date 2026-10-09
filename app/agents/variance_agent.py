from __future__ import annotations

from typing import Any


def analyze_variance(gl_summary: list[dict[str, Any]], forecast: list[dict[str, Any]]) -> dict[str, Any]:
    actual_by_account = {item["account"]: item for item in gl_summary if "account" in item}
    forecast_by_account = {item["account"]: item for item in forecast if "account" in item}

    breakdown: list[dict[str, Any]] = []
    narrative: list[str] = []
    total_variance = 0.0

    for account in sorted(set(actual_by_account) | set(forecast_by_account)):
        actual = float(actual_by_account.get(account, {}).get("amount", 0))
        plan = float(forecast_by_account.get(account, {}).get("amount", 0))
        delta = actual - plan
        total_variance += delta

        pct = round((delta / plan) * 100, 2) if plan else 0.0
        breakdown.append(
            {
                "account": account,
                "actual": actual,
                "forecast": plan,
                "delta": delta,
                "variance_pct": pct,
                "source": actual_by_account.get(account, {}).get("source_system", "unknown"),
            }
        )

        if abs(delta) > 100_000:
            direction = "above plan" if delta > 0 else "below plan"
            narrative.append(f"{account} is {direction} by ${abs(delta):,.0f} ({pct:.2f}%).")

    return {
        "total_variance": total_variance,
        "variance_breakdown": breakdown,
        "key_findings": narrative or ["No material variance exceeding tolerance threshold found."],
        "confidence": 0.92,
    }
