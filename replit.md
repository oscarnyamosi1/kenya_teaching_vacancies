# Kenya Teaching Vacancies (KTV)

A Django-based job board platform specialized for the Kenyan education sector, connecting teachers with schools and educational institutions.

## Project Overview

- **Framework:** Django 6.0 (Python 3.12)
- **API:** Django REST Framework with SimpleJWT authentication
- **Frontend:** Django Templates (server-side rendering) with HTML/CSS/JS
- **Database:** SQLite (development), PostgreSQL-ready (psycopg2-binary installed)
- **Static Files:** WhiteNoise for serving static files

## Key Features

- Job postings for teaching vacancies (TSC registration, subject specializations, curriculum types)
- Teacher profiles with document uploads (CVs, transcripts, certificates)
- Job application system
- Trending jobs logic (views, saves, application rates)
- Regional mapping of Kenyan Counties and Constituencies
- Internal messaging system
- Payment/premium job postings

## Project Structure

- `kenya_teaching_vacancies/` - Core project config (settings, URLs, WSGI)
- `main/` - Shared models (Counties, Constituencies, Subjects, Languages, Themes)
- `jobs/` - Job postings, trending logic, categories
- `teachers/` - Teacher profiles, documents, application history
- `schools/` - School profiles, categories, blogs
- `employers/` - Employer dashboards
- `applications/` - Job application process
- `api/` - REST API (DRF)
- `messagesapp/` - Internal messaging
- `payments/` - Premium listings/subscriptions
- `superuser/` - Admin utilities
- `static/` - CSS, JS, fonts, images
- `templates/` - Global templates with reusable components

## Running the App

The app runs via the "Start application" workflow:
```
python manage.py runserver 0.0.0.0:5000
```

## Development Setup

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:5000
```

## Deployment

Configured for autoscale deployment using gunicorn:
```
gunicorn --bind=0.0.0.0:5000 --reuse-port kenya_teaching_vacancies.wsgi:application
```

## Important Notes

- `ALLOWED_HOSTS = ['*']` is set in settings.py for Replit proxy compatibility
- Migrations were not included in the original repo — they are generated locally
- `main/signals.py` initializes default themes (macglass, charcoal, green) after migrations
- Signal safely checks for table existence before inserting data
