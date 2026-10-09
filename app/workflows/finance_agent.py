# agentic-finance-ops-demo

Multi-agent system for finance and operations workflows: reconciliation, variance analysis, AR/AP review, and close automation. Built with FastAPI, LangGraph, and audit-ready controls for a credible portfolio demo.

## Why this project matters
This repo was designed for a Forward Deployed Engineer interview and a client-facing AI innovation scenario. It demonstrates how finance teams can use AI to accelerate close reviews, variance analysis, and exception monitoring while preserving source traceability and a human-in-the-loop approval checkpoint.

The work is intentionally structured to feel operationally realistic rather than toy-like. It models the kinds of capability a customer would want to see in a finance transformation engagement: auditable outputs, control checkpoints, and clear source citations.

## Use cases covered
1. Quarterly close variance review
   - Compare actual GL results to forecast or budget
   - Identify material variance before management signoff
   - Produce an explanation that is traceable to source systems

2. AR/AP and working capital review
   - Highlight movement in receivables and payables
   - Surface potential cash pressure or working capital imbalance

3. Close memo and exception summary
   - Package the output into a review-ready narrative
   - Include citations and control marks suitable for finance validation

## Architecture

```text
Client / API Consumer
        |
        v
FastAPI application
        |
        +--> /health/ready
        +--> /workflow/status
        +--> /finance/analyze-variance
        +--> /finance/audit-trail
        |
        +--> LangGraph workflow
              extract -> normalize -> reconcile -> variance -> approval -> summary
              |
              +--> source citations
              +--> SOX-style control metadata
              +--> human approval checkpoint
              +--> audit log
```

## Workflow sequence
1. Extract: read actuals and forecast data from ERP and planning sources
2. Normalize: align accounts, periods, and units
3. Reconcile: compare account-level values and identify variances
4. Variance analysis: explain delta and assess materiality
5. Human approval: represent the review and signoff step required by finance controls
6. Summary: generate the final output with citations and audit evidence

## Data model and controls
- Each record remains traceable to a source system and extraction timestamp
- Every output is linked to citations and control checks
- Audit events are written for workflow actions and final summary generation
- Human approval is treated as an explicit gate before finalization

## Local run

### Python
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Compose
```bash
docker-compose up --build
```

Then open:
- http://localhost:8000/docs
- http://localhost:8000/health/ready
- http://localhost:8000/workflow/status

## Sample API request

```bash
curl -X POST "http://localhost:8000/finance/analyze-variance" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "analyst_001",
    "approval": true,
    "gl_summary": [
      {"account": "Revenue", "amount": 8725000, "source_system": "Oracle ERP GL"},
      {"account": "Payroll", "amount": 3450000, "source_system": "Oracle ERP GL"},
      {"account": "Marketing", "amount": 680000, "source_system": "Oracle ERP GL"}
    ],
    "forecast": [
      {"account": "Revenue", "amount": 8900000, "source_system": "FP&A Forecast"},
      {"account": "Payroll", "amount": 3300000, "source_system": "FP&A Forecast"},
      {"account": "Marketing", "amount": 620000, "source_system": "FP&A Forecast"}
    ]
  }'
```

## Sample API response

```json
{
  "summary": {
    "headline": "Quarter-end review completed with source citations, control checks, and a documented human approval checkpoint.",
    "status": "approved",
    "variance_total": -825000.0,
    "key_findings": [
      "Revenue is below plan by $175,000 (-1.97%)."
    ],
    "audit_id": "FIN-20261009-123456",
    "generated_at": "2026-10-09T12:34:56+00:00"
  },
  "citations": [
    {"source": "Oracle ERP GL", "record": "Revenue", "version": "variance-review"}
  ],
  "control_checks": [
    {"id": "SOX-001", "status": "pass", "description": "GL and forecast account mapping validated."},
    {"id": "SOX-003", "status": "pass", "description": "Human approval checkpoint recorded."}
  ],
  "confidence": 0.92,
  "audit_id": "FIN-20261009-123456"
}
```

## Clerk integration
This project is intentionally structured to work with a Clerk-authenticated user identity model. In a real product deployment, the audit trail would record the authenticated approver and enforce role-based access for analyst and reviewer personas.

## Deployment notes
The repo includes a base containerized deployment path and can be extended to Kubernetes, CI/CD, and environment-specific secrets management. It is ready to be used as a starting point for a client demo or a more production-hardened deployment pipeline.

## License
MIT
