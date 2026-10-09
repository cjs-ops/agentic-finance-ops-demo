# agentic-finance-ops-demo
Multi-agent system for finance & operations workflows: reconciliation, variance analysis, AR/AP, close automation. Built with FastAPI, LangGraph, and audit-ready controls.

## Why this project matters
This project presents a portfolio-ready finance workflow demo for a Forward Deployed Engineer engagement. It combines reconciliations, variance analysis, and a human approval checkpoint to demonstrate a realistic close-review pattern used in finance operations and audit support.

## What is included
- LangGraph-based workflow with extract, normalize, reconcile, variance, approval, and summary steps
- realistic GL and forecast example data with source system traceability
- audit logger with control checks and source citations
- FastAPI endpoints for health, workflow status, and variance analysis
- Docker Compose support for local execution
- Clerk-ready identity pattern for enterprise demonstration

## Example use cases
1. Quarterly close variance review
2. AR/AP and working capital review
3. Forecast-to-actual reconciliation before management signoff

## Architecture
```text
Client / API Consumer
        |
        v
FastAPI service
        |
        +--> /health/ready
        +--> /workflow/status
        +--> /finance/analyze-variance
        +--> /finance/audit-trail
        |
        +--> LangGraph workflow
              extract -> normalize -> reconcile -> variance -> approval -> summary
              |
              +--> audit logger + citations + SOX-style control markers
```

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or with Docker:
```bash
docker-compose up --build
```

## Sample API request
```bash
curl -X POST "http://localhost:8000/finance/analyze-variance" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "analyst_001",
    "approval": true,
    "gl_summary": [
      {"account": "Revenue", "amount": 8725000, "source_system": "Oracle ERP GL"},
      {"account": "Payroll", "amount": 3450000, "source_system": "Oracle ERP GL"}
    ],
    "forecast": [
      {"account": "Revenue", "amount": 8900000, "source_system": "FP&A Forecast"},
      {"account": "Payroll", "amount": 3300000, "source_system": "FP&A Forecast"}
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
    "key_findings": ["Revenue is below plan by $175,000 (-1.97%)."],
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

## Deployment notes
This repository is structured to scale into containerized deployment and can be extended to Kubernetes with health checks, secret management, and ingress policies.

## Clerk integration
This project is designed for a Clerk-backed enterprise identity pattern. The application is prepared to accept a user identity from the front end or API layer, and the audit log records the approver and action metadata.

## License
MIT
