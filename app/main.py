from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.openapi.utils import get_openapi  # ✅ Added
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

# Hardcoded API Key (replace with your generated key)
API_KEY = "c7681f2a5dee52a3e21f72db2dfbd1c8b685a45783bb8549682a4de9be0297ec"
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Dependency to enforce API key
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == f"Bearer {API_KEY}":
        return api_key_header
    raise HTTPException(
        status_code=403, detail="Could not validate API key"
    )

# ----------- Routes -----------

@app.post("/add_policy", summary="Add a new access policy")
def add_policy(policy: Policy, api_key: str = Depends(get_api_key)):
    policies.append(policy)
    logger.info(f"Added policy: {policy.name} for resource {policy.resource}")
    return {
        "message": "Policy added successfully",
        "total_policies": len(policies)
    }

@app.post("/simulate_access", summary="Simulate access decision")
def simulate_access(request: AccessRequest, api_key: str = Depends(get_api_key)):
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
def list_policies(api_key: str = Depends(get_api_key)):
    return {"policies": [p.dict() for p in policies]}

# ----------- Custom OpenAPI Schema with API Key Auth -----------

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": API_KEY_NAME,
            "description": "Enter your API key like: Bearer <API_KEY>"
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
