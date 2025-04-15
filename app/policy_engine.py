from typing import Tuple
from app.schemas import AccessRequest, Policy

def evaluate_access(request: AccessRequest, policies: list[Policy]) -> Tuple[bool, str]:
    if not request.resource:
        return False, "Missing resource in request"

    matched_policy = next((p for p in policies if p.resource.lower() == request.resource.lower()), None)

    if not matched_policy:
        return False, f"No policy found for resource: {request.resource}"

    if request.role.lower() not in [role.lower() for role in matched_policy.roles_allowed]:
        return False, "Role not permitted"

    if request.location.lower() not in [loc.lower() for loc in matched_policy.locations_allowed]:
        return False, "Location not permitted"

    # 🔐 Device trust enforcement
    trusted_levels = ["trusted", "high"]
    if matched_policy.trusted_devices_only and request.device_trust_level.lower() not in trusted_levels:
        return False, "Untrusted device"

    if request.action.lower() not in [act.lower() for act in matched_policy.actions]:
        return False, "Action not permitted"

    return True, "Access granted based on matching policy"
