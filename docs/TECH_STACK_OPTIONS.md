# Technology Stack Options

This repository **implements Option A** in full (it's what's in `backend/`
and `frontend/`). Options B and C describe how to evolve it.

## Option A — Beginner (implemented here)
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Backend:** Python Flask (`backend/app.py`)
- **Database:** SQLite (`backend/database.py`)
- **Storage:** Local uploads folder (`backend/storage_service.py`)
- **Difficulty:** Low · **Cost:** $0
- **Concepts demonstrated:** REST API, RBAC, client-server architecture,
  metadata/object separation (in miniature), deadline logic, testing.
- **Advantages:** Zero setup cost, runs entirely offline, easy to grade/demo.
- **Limitations:** Not horizontally scalable, single point of failure, no
  real cloud infra to point to in an interview beyond "the code is written
  to swap in cloud services."

## Option B — Recommended Cloud Version
- **Frontend:** React
- **Backend:** Python FastAPI or Flask (same code shape as Option A)
- **Authentication:** Firebase Authentication or Supabase Auth
- **Database:** Firestore or Supabase PostgreSQL
- **Cloud Storage:** Firebase Storage or Supabase Storage
- **Deployment:** Netlify/Vercel (frontend) + Render/Railway (backend)
- **Difficulty:** Medium · **Cost:** $0 on free tiers for a student project
- **Concepts demonstrated:** everything in Option A, plus real managed cloud
  database, real managed object storage, and a real public URL.
- **Advantages:** A genuine cloud deployment link for your resume/GitHub.
- **Limitations:** Free-tier quotas (storage size, DB rows, bandwidth) —
  fine for a course project, not for real traffic.

## Option C — Advanced Cloud Version
- **Frontend:** React / Next.js on S3+CloudFront (or Vercel)
- **Backend:** FastAPI on AWS Lambda / App Runner (or Azure/GCP equivalents)
- **Database:** RDS / DynamoDB
- **Storage:** S3
- **Auth:** Cognito
- **API:** API Gateway in front of the serverless functions
- **Monitoring:** CloudWatch
- **Difficulty:** High · **Cost:** Usually still free-tier-eligible for a
  low-traffic student demo, but requires a credit card on file with the
  provider.
- **Concepts demonstrated:** the full IaaS/PaaS/serverless spectrum, API
  Gateway, managed autoscaling.
- **Advantages:** Closest to how a real EdTech company would build this.
- **Limitations:** Steepest learning curve; easiest to accidentally incur
  costs if free-tier limits are exceeded.

## Recommendation
**Option B** is the best fit for a student aiming for GitHub proof-of-work:
it is genuinely deployed on real cloud services, stays free, and takes a
manageable step up from Option A (which this repo already gives you a
complete, tested starting point for).
