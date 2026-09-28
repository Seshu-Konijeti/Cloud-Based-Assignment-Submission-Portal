# Scalability

## At 10 students
The current architecture (single Flask process + SQLite + local disk) is
more than sufficient. This is the "Option A" free/local setup.

## At 1,000 students
- Move the database to a managed cloud database (Postgres on Supabase/RDS) —
  SQLite is single-writer and not designed for concurrent access from
  multiple backend instances.
- Move file storage to S3/Firebase Storage instead of local disk, since a
  single server's disk won't survive a redeploy and can't be shared across
  multiple backend instances.
- Run 2+ backend instances behind a **load balancer** for redundancy.

## At 100,000 students (e.g., all uploading near one deadline)
- **Load balancer** distributes incoming requests across many backend
  instances.
- **Autoscaling** spins up additional backend instances automatically as
  request volume rises around the deadline, and scales back down after.
- **Serverless functions** (Lambda/Cloud Functions) can absorb bursty upload
  traffic without pre-provisioning fixed servers.
- **Managed database** (RDS/DynamoDB/Firestore) handles connection pooling
  and read replicas so metadata writes/reads don't bottleneck.
- **Object storage** (S3/Firebase Storage) scales storage and throughput
  independently of the database — genuinely limitless for this workload.
- **CDN** serves the static frontend assets from edge locations close to
  each student, keeping page loads fast regardless of total user count.
- **Caching** (e.g. Redis) for read-heavy, rarely-changing data such as the
  assignment list, so repeated dashboard loads don't all hit the database.
- **Message queues + background workers** — instead of validating/scanning
  a file synchronously during the HTTP request, the upload could enqueue a
  background job (virus scan, thumbnail generation, notification email),
  keeping the upload response fast even under load.

## Example: 100,000 students uploading near a deadline
The load balancer spreads the burst of `POST /assignments/{id}/submit`
requests across an autoscaled fleet of backend instances. Each instance
writes the file straight to S3 (which can absorb effectively unlimited
concurrent writes) and a small metadata row to the managed database.
Heavier post-processing (e.g. malware scanning) is pushed onto a queue so
the student's browser gets a fast "Submission received" response instead of
waiting on that work synchronously.
