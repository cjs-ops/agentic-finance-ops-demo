import streamlit as st

st.set_page_config(page_title="Finance Ops Demo", page_icon="💼", layout="wide")

st.title("Finance Ops Demo")
st.caption("Variance analysis, reconciliation checks, and audit-ready summaries")

if st.button("Run variance review"):
    sample_gl = [
        {"account": "Revenue", "amount": 8_725_000, "source_system": "Oracle ERP GL"},
        {"account": "Payroll", "amount": 3_450_000, "source_system": "Oracle ERP GL"},
        {"account": "Marketing", "amount": 680_000, "source_system": "Oracle ERP GL"},
    ]
    forecast = [
        {"account": "Revenue", "amount": 8_900_000, "source_system": "FP&A Forecast"},
        {"account": "Payroll", "amount": 3_300_000, "source_system": "FP&A Forecast"},
        {"account": "Marketing", "amount": 620_000, "source_system": "FP&A Forecast"},
    ]

    from app.agents.reconciliation_agent import reconcile_gl_to_forecast
    from app.agents.variance_agent import analyze_variance

    reconciliation = reconcile_gl_to_forecast(sample_gl, forecast)
    variance = analyze_variance(sample_gl, forecast)

    st.subheader("Variance summary")
    st.write({
        "status": reconciliation["status"],
        "total_variance": variance["total_variance"],
        "key_findings": variance["key_findings"],
    })

    st.subheader("Audit controls")
    st.json(reconciliation["control_checks"])
