# zero-trust-access-simulator

## 🛡️ Zero Trust Access Policy Simulator – Documentation

### 📘 Overview

The **Zero Trust Access Policy Simulator** is a FastAPI-based tool designed to simulate and evaluate access decisions based on user attributes, contextual data, and defined policies. It follows Zero Trust principles, ensuring that **no access is granted by default**—access is explicitly evaluated against fine-grained policies.

---

### 🧐 What is Zero Trust?

**Zero Trust** is a security model that assumes no user or system should be trusted by default—even if inside the network perimeter. Access must be **continuously verified** based on multiple contextual factors such as:
- User identity and role
- Device posture (e.g., trusted or not)
- Geographic location
- Requested action and resource

---

### ⚠️ Real-World Challenges Zero Trust Tries to Solve

#### 1. **Insider Threats**
Traditional security assumes users inside the network are trusted. Zero Trust treats every user as potentially malicious.

**How this project helps:** You can define policies that restrict actions based on user roles and device trust level.

#### 2. **Cloud Misconfigurations**
Data in the cloud is often exposed due to overly permissive access.

**How this project helps:** You simulate granular policies before applying them to cloud environments—preventing "over-permissioned" access.

#### 3. **Remote Work Risk**
Remote access introduces new attack surfaces.

**How this project helps:** Simulations can reject access from untrusted devices or geographies.

#### 4. **Data Exfiltration**
Users downloading or leaking sensitive data.

**How this project helps:** Define `actions` and `resources` explicitly, simulate before granting access.

---

### 🔐 Features

- ✅ Middleware logging of all requests with metadata
- ✅ API key protection for all routes
- ✅ Expiring policies support (`expires_at`)
- ✅ Contextual policy matching (role, location, device, etc.)
- ✅ Real-time access simulation
- ✅ Swagger/OpenAPI documentation secured with API key

---

### 👩️‍💻 For Developers & Security Teams

#### 📦 Installation

```bash
git clone https://github.com/your-username/zero-trust-simulator.git
cd zero-trust-simulator
pip install -r requirements.txt
uvicorn main:app --reload
```

#### 🔐 Using the API

**Step 1:** Add your API key in the Swagger UI like:

```
Bearer c7681f2a5dee52a3e21f72db2dfbd1c8b685a45783bb8549682a4de9be0297ec
```

---

#### 📜 Example: Add Policy

```json
POST /add_policy

{
  "name": "File Access Policy",
  "roles_allowed": ["admin", "manager"],
  "locations_allowed": ["NYC", "London"],
  "trusted_devices_only": true,
  "resource": "file1.txt",
  "actions": ["read", "write"],
  "expires_at": "2025-05-01T00:00:00Z"
}
```

---

#### 🧪 Example: Simulate Access

```json
POST /simulate_access

{
  "user_id": "john_doe",
  "role": "admin",
  "location": "NYC",
  "device_trust_level": "trusted",
  "resource": "file1.txt",
  "action": "read"
}
```

Response:

```json
{
  "access_granted": true,
  "reason": "Access granted based on matching policy",
  "user": "john_doe",
  "resource": "file1.txt",
  "action": "read"
}
```

---

### 📊 Use Cases

- 🛡️ Internal security simulation for Zero Trust adoption
- 🧪 Security control validation before policy deployment
- 🌐 Cloud access audit tools
- 👨‍💻 Developer tools to test IAM logic

---

### 🚳️ Known Issues / Limitations

- In-memory storage: policies are not persistent (can be extended to DB)
- No user authentication/authorization outside API key (can be added via OAuth2)
- Doesn’t simulate real-time traffic or integrate with SIEM yet

---

### 🌍 Real-World Applications

- Financial institutions simulating fine-grained access before deployment
- Cloud migration teams verifying policies to prevent S3/GCS misconfig
- Enterprises adopting Zero Trust with remote workers and BYOD devices

