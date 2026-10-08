# Deployment guide

This repository is designed to run locally with Docker Compose and extend to a Kubernetes deployment model.

## Local container run
```bash
docker-compose up --build
```

## Representative Kubernetes deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: finance-ops-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: finance-ops-demo
  template:
    metadata:
      labels:
        app: finance-ops-demo
    spec:
      containers:
        - name: api
          image: finance-ops-demo:latest
          ports:
            - containerPort: 8000
          env:
            - name: CLERK_PUBLISHABLE_KEY
              value: "pk_test_demo"
            - name: CLERK_SECRET_KEY
              value: "sk_test_demo"
---
apiVersion: v1
kind: Service
metadata:
  name: finance-ops-demo
spec:
  selector:
    app: finance-ops-demo
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```

## Recommended production hardening
- Add health checks for `/health/ready` and `/workflow/status`.
- Store all secrets in a managed secret store, not in source control.
- Add separate Kubernetes namespaces for dev/test/prod.
- Integrate OpenTelemetry or logging agents for audit trail observability.
- Enforce approval roles before final variance signoff in a real client deployment.
