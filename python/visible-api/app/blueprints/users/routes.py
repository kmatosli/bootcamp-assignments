from flask import request, jsonify
from app.blueprints.users import users_bp
from app.blueprints.users.schemas import user_schema, users_schema, user_login_schema
from app.models import VisibleUser, CareerSession
from app.extensions import db, cache, limiter
from app.utils.auth import encode_token, token_required
import re

def valid_email(email):
    return re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email)

# GET /users
@users_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
@limiter.limit("30 per minute")
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = VisibleUser.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'users': users_schema.dump(users.items),
        'total': users.total,
        'pages': users.pages,
        'page': users.page
    }), 200

# GET /users/<id>
@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(VisibleUser, id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return user_schema.jsonify(user), 200

# POST /users
@users_bp.route('/', methods=['POST'])
@limiter.limit("10 per minute")
def create_user():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('name'):
        return jsonify({'error': 'Name and email are required'}), 400
    if not valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    if VisibleUser.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    user = VisibleUser(
        name=data['name'],
        email=data['email'],
        password=data.get('password', ''),
        job_title=data.get('job_title', ''),
        company=data.get('company', '')
    )
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

# PUT /users/<id>
@users_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_user(user_id, id):
    user = db.session.get(VisibleUser, id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    for field in ['name', 'job_title', 'company']:
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return user_schema.jsonify(user), 200

# DELETE /users/<id>
@users_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_user(user_id, id):
    user = db.session.get(VisibleUser, id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

# POST /users/login
@users_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    errors = user_login_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user = VisibleUser.query.filter_by(email=data['email']).first()
    if not user or user.password != data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401
    token = encode_token(user.id)
    return jsonify({'token': token, 'user_id': user.id}), 200

# GET /users/my-sessions
@users_bp.route('/my-sessions', methods=['GET'])
@token_required
def my_sessions(user_id):
    sessions = CareerSession.query.filter_by(user_id=user_id).all()
    from app.blueprints.sessions.schemas import sessions_schema
    return sessions_schema.jsonify(sessions), 200