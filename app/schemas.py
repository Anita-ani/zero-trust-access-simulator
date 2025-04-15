from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AccessRequest(BaseModel):
    user_id: str
    role: str
    location: str
    device_trust_level: str
    resource: str
    action: str

class Policy(BaseModel):
    name: str
    roles_allowed: list[str]
    locations_allowed: list[str]
    trusted_devices_only: bool
    resource: str
    actions: list[str]
    expires_at: Optional[datetime] = None  # Optional expiration
