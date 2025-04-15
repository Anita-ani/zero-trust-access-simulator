from fastapi import FastAPI
from app.policy_engine import evaluate_access
from app.schemas import AccessRequest, Policy
from app.logger import logger
from app.middleware import RequestLoggingMiddleware

app = FastAPI(
    title="Zero Trust Access Policy Simulator",
    description="Simulates access decisions based on user context and policy",
    version="0.1.0"
)

# Register middleware to log request metadata
app.add_middleware(RequestLoggingMiddleware)

# ----------- In-Memory Policy Store -----------
policies: list[Policy] = []

# ----------- Routes -----------

@app.post("/add_policy", summary="Add a new access policy")
def add_policy(policy: Policy):
    policies.append(policy)
    logger.info(f"Added policy: {policy.name} for resource {policy.resource}")
    return {
        "message": "Policy added successfully",
        "total_policies": len(policies)
    }

@app.post("/simulate_access", summary="Simulate access decision")
def simulate_access(request: AccessRequest):
    decision, reason = evaluate_access(request, policies)

    logger.info(
        f"[ACCESS CHECK] User={request.user_id}, Role={request.role}, "
        f"Location={request.location}, Device={request.device_trust_level}, "
        f"Resource={request.resource}, Action={request.action}, "
        f"Granted={decision}, Reason={reason}"
    )

    return {
        "access_granted": decision,
        "reason": reason,
        "user": request.user_id,
        "resource": request.resource,
        "action": request.action
    }

@app.get("/list_policies", summary="List all defined policies")
def list_policies():
    return {"policies": [p.dict() for p in policies]}
