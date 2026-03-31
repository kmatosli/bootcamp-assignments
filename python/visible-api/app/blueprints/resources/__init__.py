from flask import Blueprint
resources_bp = Blueprint('resources', __name__)
from app.blueprints.resources import routes
