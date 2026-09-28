# Cloud Deployment

## Local Development vs Cloud Deployment
| | Local Development | Cloud Deployment |
|---|---|---|
| Database | SQLite file on disk | Managed Postgres/Firestore/DynamoDB |
| Storage | `backend/storage/` folder | S3 / Firebase Storage / Supabase Storage |
| Access | `localhost` only | Public HTTPS URL, reachable from anywhere |
| Scaling | Single process | Autoscaled instances / serverless functions |
| Secrets | `.env` file (git-ignored) | Platform's secrets manager / environment config |

## Approach A — Free-Tier / Student-Friendly
1. **Frontend** — deploy the static `frontend/` folder to Netlify, Vercel, or GitHub Pages (all free).
2. **Backend** — deploy `backend/` (Flask) to Render.com or Railway.app free tier; set the same variables from `.env.example` in their dashboard.
3. **Database** — swap `DATABASE_URL` to a free Supabase Postgres instance or Render's free Postgres add-on.
4. **Storage** — swap `STORAGE_BACKEND` to a free-tier Supabase Storage bucket or Firebase Storage (Spark plan).
5. **Authentication** — the built-in JWT system works as-is; optionally swap for Firebase Auth's free tier for social login.

## Approach B — AWS/Azure/GCP Architecture
| Component | AWS | Azure (equivalent) | GCP (equivalent) |
|---|---|---|---|
| Frontend | S3 + CloudFront | Static Web Apps + Front Door | Cloud Storage + Cloud CDN |
| Backend | Lambda / App Runner / EC2 | Azure Functions / App Service | Cloud Functions / Cloud Run |
| API | API Gateway | API Management | API Gateway |
| Database | RDS (Postgres) / DynamoDB | Azure SQL / Cosmos DB | Cloud SQL / Firestore |
| Files | S3 | Blob Storage | Cloud Storage |
| Auth | Cognito | Azure AD B2C | Firebase Auth / Identity Platform |
| Logs | CloudWatch | Monitor / Log Analytics | Cloud Logging |

## Recommended CI/CD (GitHub Actions, conceptual)
```
on: push to main
  1. Checkout code
  2. Install dependencies
  3. Run pytest
  4. Build frontend (if applicable)
  5. Deploy backend to Render/Railway
  6. Deploy frontend to Netlify/Vercel
```
This turns every merge to `main` into an automatic, tested deployment —
the CI/CD concept required by the brief.

## Monitoring
- `GET /api/health` is a ready-made endpoint for uptime monitors (UptimeRobot,
  the hosting platform's own health checks, or a CloudWatch synthetic canary).
