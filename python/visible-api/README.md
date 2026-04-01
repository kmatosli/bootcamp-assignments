# Visible API — Career Intelligence REST API

A Flask REST API built with the Application Factory Pattern, Blueprints, SQLAlchemy, and Marshmallow.

## Setup Instructions

1. Clone the repository and navigate to this folder:
   cd python/visible-api

2. Install dependencies:
   pip install -r requirements.txt

3. Initialize the database:
   python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"

4. Run the app:
   python -m flask --app app:create_app run

## Endpoints

- GET/POST /advisors
- GET/PUT/DELETE /advisors/<id>
- POST /advisors/login
- GET/POST /users
- GET/PUT/DELETE /users/<id>
- POST /users/login
- GET /users/my-sessions
- GET/POST /resources
- GET/PUT/DELETE /resources/<id>
- GET/POST /sessions
- GET/PUT/DELETE /sessions/<id>
- GET/POST /inventory
- GET/PUT/DELETE /inventory/<id>

## Tech Stack
- Flask + Application Factory Pattern
- SQLAlchemy + SQLite
- Marshmallow schemas
- JWT authentication (python-jose)
- Flask-Limiter for rate limiting
- Flask-Caching
