This file documents how to deploy the G-Bridge project to Render.com.

Overview
--------
This repository contains a Django backend (in `backend/`) and a Vite React frontend (in `frontend/`).

Render blueprint
----------------
A `render.yaml` blueprint is included at the repository root. It defines:
- A web service `g-bridge-backend` (Python) that uses `./build.sh` in the repo root to install backend dependencies and starts with Gunicorn. The `releaseCommand` runs database migrations and `collectstatic`.
- A static site `g-bridge-frontend` that builds the frontend using `npm ci && npm run build` and publishes `dist` from the `frontend` directory.
 - No managed database is required by default; the project uses SQLite locally. You may provision a managed database and set `DATABASE_URL` if desired.

Required environment variables
------------------------------
Set these in the Render dashboard for the backend service (or mark as secrets via the UI):
- SECRET_KEY (secret)
- DATABASE_URL (secret) — Optional. If you provide this, the service will use the specified database instead of the default SQLite file.
- CLIENT_ID (secret) — Google OAuth client id used by the app.
- CLIENT_SECRET (secret)
- REFRESH_TOKEN (secret)
- GOOGLE_DRIVE_FOLDER_ID (secret)
- ALLOWED_HOSTS — comma-separated; can be left empty (defaults to `*`).
- DEBUG — set to `False` in production.
- FRONTEND_ORIGINS — optional, used to configure CORS.
- CSRF_TRUSTED_ORIGINS — optional.

Steps to deploy on Render
-------------------------
1. Sign in to Render and create a new Web Service from the GitHub repo `rahomi/G-Bridge`.
2. Choose branch `main` and the `render.yaml` blueprint to create all services at once (web, static, database). Review names and plans.
3. For the backend service, ensure the `env` is Python. Render will run `./build.sh` during build and the `releaseCommand` before starting instances.
4. For the static site, review `VITE_API_URL` in the static site's env vars. Replace `https://<your-backend>.onrender.com` with the backend service's URL (Render will provide it after deploy).
5. Add required secrets in the Service > Environment section.
6. Deploy. The `releaseCommand` will run migrations and collectstatic before the web service starts.

Notes & troubleshooting
-----------------------
- Database: By default the project uses SQLite. If you provide a `DATABASE_URL`, ensure it points to a compatible database and migrations are run during deployment.
- Static files: `whitenoise` is configured and `collectstatic` stores files in `staticfiles`.
- Health check: `render.yaml` sets `healthCheckPath: /api/health/`. Ensure this endpoint exists and returns 200.
- Local testing: You can run migrations and the dev server locally with `pip install -r backend/requirements.txt`, `python backend/manage.py migrate`, then `python backend/manage.py runserver`.

If you want, I can also:
- Add a simple `/api/health/` view if it's missing.
- Wire `VITE_API_URL` as a Render secret and update the blueprint with the actual backend URL after first deploy.

Requirements coverage: I updated `render.yaml` and `build.sh` and provided a deployment guide.

