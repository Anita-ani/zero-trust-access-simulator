# app/policies.py

POLICIES = {
    "financial_reports": {
        "allowed_roles": ["manager", "auditor"],
        "locations": ["Lagos", "Abuja"],
        "device_trust_levels": ["high", "medium"],
        "actions": ["read", "download"]
    },
    # add more resources...
}
