# Urban Logistics App

A Flask operations dashboard for managing orders, delivery partners, and delivery status workflows.

## Current Features

- Dashboard KPIs for total orders, active deliveries, and active partners
- Order creation with existing or new customers
- Automatic delivery partner assignment by hub and active capacity
- Delivery status history with guarded state transitions
- Partner activation/deactivation service rules
- Alembic/Flask-Migrate database migrations

## Setup

Create a virtual environment outside source control:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

For local development, the app can use SQLite through `DATABASE_URL=sqlite:///urban_logistics.db`.

Initialize the database:

```powershell
flask db upgrade
python scripts\seed.py
```

Run the app:

```powershell
flask run
```

Open `http://127.0.0.1:5000`.

## Tests

```powershell
pytest
```

## Notes

- Do not commit `venv/`, `.venv/`, `.env`, local database files, or `__pycache__/`.
- The original archive included a machine-specific `venv`; recreate the environment locally instead.
- Production should use a real `SECRET_KEY`, a managed PostgreSQL database, HTTPS, and authentication.
