# Sanzalibrary

Sanzalibrary is a Django-based digital library and reading platform that lets users browse books, view categories, manage a personal library, read book details, and access role-based admin/author workflows.

This project includes the core app logic and a premium UI redesign layered on top of the existing Django templates without rewriting backend behavior.

## Project overview

- Framework: Django
- Database: SQLite
- Primary app: `book/`
- Main settings: `ebook/settings.py`
- Templates: `templates/`
- Static assets: `static/`
- Media uploads: `media/`

## Main features

- Browse and search books
- View categories and category-based book listings
- View detailed book pages
- Free and paid book flows
- User authentication and registration
- Admin/author management screens
- Contact form and company pages
- Premium responsive design system based on the reference mockups in `stitch_premium_digital_library_platform/`

## Repository structure

```text
E-library/
├── book/
│   ├── management/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── adapters.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── ebook/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/
├── static/
├── templates/
│   ├── account/
│   ├── category/
│   ├── company/
│   └── ...
├── db.sqlite3
├── manage.py
├── requirements.txt
├── set_all_category_images.py
├── stitch_premium_digital_library_platform/
└── README.md
```

## Technologies used

- Python
- Django
- SQLite
- HTML / CSS / JavaScript
- Django template system
- Font Awesome and Google Fonts for UI styling

## Environment setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply database migrations:

```bash
python manage.py migrate
```

4. Create a superuser if needed:

```bash
python manage.py createsuperuser
```

## Run the project

Start the local development server:

```bash
python manage.py runserver 0.0.0.0:8000
```

Then open:

```text
http://localhost:8000/
```

## Useful Django commands

```bash
# Run the app
python manage.py runserver

# Run migrations
python manage.py migrate

# Make new migrations after model changes
python manage.py makemigrations

# Open shell
python manage.py shell

# Run tests
python manage.py test
```

## Admin and management notes

The project includes admin/author management interfaces and role-based logic. These routes and templates are designed to work with the existing backend logic without requiring any major rewrite of the application behavior.

## Premium UI redesign status

The active front-end layer is being updated to follow the design reference under:

```text
stitch_premium_digital_library_platform/
```

The design goal is to keep the original app behavior, routes, and backend logic intact while aligning the visual language with the premium reference mockups.

## Notes

- Static files and media are stored in `static/` and `media/` respectively.
- The app currently uses SQLite for local development.
- Most UI changes are template-based and therefore safe to apply without changing the data model or route structure.

## Recommended next steps

- Review the home, books, detail, auth, and dashboard templates for final style polishing.
- Check responsiveness across mobile and tablet widths.
- Validate that admin, author, and user flows still work after styling updates.
- Add production deployment settings and environment configuration when preparing for hosting.
