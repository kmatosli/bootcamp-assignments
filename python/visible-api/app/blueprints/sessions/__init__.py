from flask import Blueprint
sessions_bp = Blueprint('sessions', __name__)
from app.blueprints.sessions import routes
