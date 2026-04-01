from flask import Flask
from app.extensions import db, ma, limiter, cache

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visible.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CACHE_TYPE'] = 'SimpleCache'

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    from app.blueprints.advisors import advisors_bp
    from app.blueprints.resources import resources_bp
    from app.blueprints.sessions import sessions_bp
    from app.blueprints.users import users_bp
    from app.blueprints.inventory import inventory_bp

    app.register_blueprint(advisors_bp, url_prefix='/advisors')
    app.register_blueprint(resources_bp, url_prefix='/resources')
    app.register_blueprint(sessions_bp, url_prefix='/sessions')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app
