# Drive Upload App

A full-stack project with a Django + DRF backend and a React (Vite) frontend. The app uploads files to a specific Google Drive folder and stores metadata in a local SQLite database by default.

## ✅ Backend features
- Django + DRF API endpoint for multipart uploads
- Google Drive API v3 upload with environment-based OAuth
- Database: uses SQLite locally. Optional `DATABASE_URL` environment variable is supported but Postgres is not required.
- Render-ready setup with `gunicorn`, `whitenoise`, and `build.sh`

## ✅ Frontend features
- React + Tailwind UI using shadcn/ui components
- File input, upload button, toast notifications
- Displays the resulting `web_view_link`

## Environment variables
Copy `.env.example` and fill in the values:

```bash
cp .env.example .env
```

Required Google OAuth values:
- `CLIENT_ID`
- `CLIENT_SECRET`
- `REFRESH_TOKEN`
- `GOOGLE_DRIVE_FOLDER_ID`

## Local development

### Backend

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL` in `frontend/.env` if your API URL differs (default `http://localhost:8000`).

## Render deployment notes
- Use `build.sh` for the build command.
- Set the start command to:

```bash
gunicorn backend.wsgi:application --chdir backend
```

If you deploy to a hosted provider, configure a database there if you prefer Postgres in production. The project runs fine using SQLite (default). When deploying, set `ALLOWED_HOSTS` to your host and `DEBUG=False`.

## API endpoint
`POST /api/upload/` expects `multipart/form-data` with a `file` field. It returns the saved `DriveFile` record.
