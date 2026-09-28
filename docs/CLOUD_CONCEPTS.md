# Cloud Computing Concepts Demonstrated

| Concept | Where it appears in this project |
|---|---|
| **Cloud Computing (general)** | The app is designed so its DB, storage, and auth are all externally-hosted, swappable services rather than parts baked into one server. |
| **SaaS** | The deployed portal itself, delivered to students/teachers over the browser with zero local install. |
| **PaaS** | The recommended deployment targets (Render/Railway/Vercel for backend, Netlify/Vercel for frontend) are Platform-as-a-Service — you push code, the platform handles the OS/runtime. |
| **IaaS concepts** | Covered conceptually in `docs/DEPLOYMENT.md` (Option C: raw EC2/VMs you'd manage yourself). |
| **Cloud Database** | `backend/database.py` + `backend/models.py`. SQLite locally; one env-var swap to Postgres/Firestore/DynamoDB in the cloud. |
| **Object Storage** | `backend/storage_service.py`. Local filesystem locally; same interface swaps to S3/Firebase Storage. |
| **Authentication** | `backend/auth_utils.py`, `routes/auth_routes.py` — JWT-based login/register. |
| **Authorization / RBAC** | `role_required()` decorator + ownership checks in every route (see `docs/SECURITY.md`). |
| **REST API** | All 20+ endpoints in `backend/routes/` — see `docs/API_DOCUMENTATION.md`. |
| **Client-Server Architecture** | `frontend/` (client) talks only to `backend/` (server) over HTTP/JSON — never touches the DB or files directly. |
| **Serverless Computing** | Discussed in `docs/DEPLOYMENT.md` Approach B: how `backend/app.py`'s routes map 1:1 onto AWS Lambda functions behind API Gateway. |
| **Scalability / Elasticity** | `docs/SCALABILITY.md` — how the same code scales from 10 to 100,000 students. |
| **Availability** | Managed cloud DB/storage replicate data across zones; discussed in `docs/SCALABILITY.md`. |
| **Load Balancing** | Sits in front of multiple backend instances once traffic grows — see `docs/SCALABILITY.md`. |
| **CDN** | Used to serve the static `frontend/` assets globally with low latency — see `docs/DEPLOYMENT.md`. |
| **API Gateway** | Fronts serverless deployments, handles routing/throttling/auth before requests reach backend code. |
| **Environment Variables** | `.env.example` — every secret and config value is externalized. |
| **Secrets Management** | Never hardcoded; loaded via `os.environ` in `config.py`. Production: a secrets manager (AWS Secrets Manager / GCP Secret Manager). |
| **Logging** | Flask's built-in request logging + error handlers in `app.py`; production would ship logs to CloudWatch/Cloud Logging. |
| **Monitoring** | `/api/health` endpoint for uptime checks; discussed further in `docs/DEPLOYMENT.md`. |
| **Backup** | Managed DB/storage automated backups — see `docs/SECURITY.md`. |
| **CI/CD** | Recommended GitHub Actions pipeline (test → build → deploy) described in `docs/DEPLOYMENT.md`. |
| **Cloud Deployment** | Full walkthrough in `docs/DEPLOYMENT.md`. |
