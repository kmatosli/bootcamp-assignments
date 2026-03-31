from flask import request, jsonify
from app.blueprints.advisors import advisors_bp
from app.blueprints.advisors.schemas import advisor_schema, advisors_schema, advisor_login_schema
from app.models import Advisor, CareerSession
from app.extensions import db, limiter
from app.utils.auth import encode_advisor_token, advisor_token_required

# GET /advisors
@advisors_bp.route('/', methods=['GET'])
def get_advisors():
    advisors = Advisor.query.outerjoin(
        Advisor.sessions
    ).group_by(Advisor.id).order_by(
        db.func.count(CareerSession.id).desc()
    ).all()
    return advisors_schema.jsonify(advisors), 200

# GET /advisors/<id>
@advisors_bp.route('/<int:id>', methods=['GET'])
def get_advisor(id):
    advisor = db.session.get(Advisor, id)
    if not advisor:
        return jsonify({'error': 'Advisor not found'}), 404
    return advisor_schema.jsonify(advisor), 200

# POST /advisors
@advisors_bp.route('/', methods=['POST'])
@limiter.limit("10 per minute")
def create_advisor():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('name'):
        return jsonify({'error': 'Name and email are required'}), 400
    if Advisor.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    advisor = Advisor(
        name=data['name'],
        email=data['email'],
        password=data.get('password', ''),
        specialty=data.get('specialty', '')
    )
    db.session.add(advisor)
    db.session.commit()
    return advisor_schema.jsonify(advisor), 201

# PUT /advisors/<id>
@advisors_bp.route('/<int:id>', methods=['PUT'])
@advisor_token_required
def update_advisor(advisor_id, id):
    advisor = db.session.get(Advisor, id)
    if not advisor:
        return jsonify({'error': 'Advisor not found'}), 404
    data = request.get_json()
    for field in ['name', 'specialty']:
        if field in data:
            setattr(advisor, field, data[field])
    db.session.commit()
    return advisor_schema.jsonify(advisor), 200

# DELETE /advisors/<id>
@advisors_bp.route('/<int:id>', methods=['DELETE'])
@advisor_token_required
def delete_advisor(advisor_id, id):
    advisor = db.session.get(Advisor, id)
    if not advisor:
        return jsonify({'error': 'Advisor not found'}), 404
    db.session.delete(advisor)
    db.session.commit()
    return jsonify({'message': 'Advisor deleted'}), 200

# POST /advisors/login
@advisors_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    errors = advisor_login_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    advisor = Advisor.query.filter_by(email=data['email']).first()
    if not advisor or advisor.password != data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401
    token = encode_advisor_token(advisor.id)
    return jsonify({'token': token, 'advisor_id': advisor.id}), 200
