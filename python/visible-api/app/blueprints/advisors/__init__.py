from flask import Blueprint
advisors_bp = Blueprint('advisors', __name__)
from app.blueprints.advisors import routes
