# Kenya Teaching Vacancies (KTV)

A full-stack job board platform for the Kenyan education sector, connecting teachers with schools. Built with Django REST API backend and React + Vite frontend.

## Project Overview

- **Backend:** Django 6.0 (Python 3.12) + Django REST Framework
- **Frontend:** React 18 + Vite (JSX), dark glassmorphism UI theme
- **Database:** SQLite (development)
- **Auth:** Django session-based auth via DRF (CSRF + cookies)

## Architecture

- **Django API** runs on `localhost:8000` (console workflow) — serves all `/api/` endpoints
- **React frontend** runs on `0.0.0.0:5000` (webview workflow) — proxies `/api` and `/media` to Django

## Key Features

- Job feed with search, filters (county, curriculum, TSC required, urgent)
- Job detail view with apply + save actions
- Teacher registration/login with session auth
- Saved jobs and My Applications pages
- Trending jobs sidebar
- Schools directory
- Teacher profile editor
- Responsive dark glassmorphism design

## Important Model Notes (Django)

- `County.title` — NOT `County.name` (use `county__title` in filters/serializers)
- `Constituency.title` — NOT `Constituency.name`
- `SchoolCategory.title` — NOT `SchoolCategory.name`
- `SchoolSponsor.title` — school sponsor type
- `School.school_type` → FK to `SchoolSponsor` (NOT SchoolCategory)
- `School.category` → FK to `SchoolCategory`
- `Job.carriculum_type` — note: intentional typo in original model

## Project Structure

- `kenya_teaching_vacancies/` — Django project config (settings, URLs, WSGI)
- `main/` — Shared models: County, Constituency, Subject, EmploymentType, Specialization, Language, Theme
- `jobs/` — Job model, trending logic
- `teachers/` — Teacher profiles, documents
- `schools/` — School, SchoolCategory, SchoolSponsor, SchoolBlog
- `employers/` — Employer model (linked to School + User)
- `applications/` — JobApplication model
- `api/` — All DRF serializers, views, URLs
- `frontend/` — React + Vite app
  - `src/pages/` — JobFeed, JobDetail, SavedJobs, MyApplications, TeacherProfile, Schools, Login, Register, NotFound
  - `src/components/` — NavBar, SideNav, Layout, JobCard, TrendingJobs
  - `src/contexts/AuthContext.jsx` — Session auth state
  - `src/api/client.js` — Axios client with CSRF interceptor

## Running the App

Two workflows must both be running:

1. **Django API** — `python manage.py runserver localhost:8000`
2. **Start application** — `cd frontend && npm run dev` (port 5000)

## Seed Data

Run to populate test data:
```bash
python manage.py shell < seed_script.py
```
Schools: Alliance High, Starehe Boys, Mombasa Academy, Kisumu Day, Riara Group
Jobs: 8 teaching vacancies across Nairobi, Mombasa, Kisumu

## Admin Access

- URL: `http://localhost:8000/admin/`
- Username: `admin` / Password: `admin123`

## Settings Highlights

- `ALLOWED_HOSTS = ['*']`
- `CORS_ALLOW_ALL_ORIGINS = True`, `CORS_ALLOW_CREDENTIALS = True`
- `SESSION_COOKIE_SAMESITE = 'Lax'`
- Vite proxy: `/api` → `http://localhost:8000`

## Deployment

Configured for autoscale deployment using gunicorn:
```
gunicorn --bind=0.0.0.0:5000 --reuse-port kenya_teaching_vacancies.wsgi:application
```
