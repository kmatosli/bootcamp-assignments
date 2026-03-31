from flask import request, jsonify
from app.blueprints.sessions import sessions_bp
from app.blueprints.sessions.schemas import session_schema, sessions_schema
from app.models import CareerSession, Advisor, Resource
from app.extensions import db, limiter
from app.utils.auth import token_required

# POST /sessions
@sessions_bp.route('/', methods=['POST'])
@token_required
def create_session(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    session = CareerSession(
        focus=data.get('focus', ''),
        notes=data.get('notes', ''),
        user_id=user_id
    )
    db.session.add(session)
    db.session.commit()
    return session_schema.jsonify(session), 201

# GET /sessions
@sessions_bp.route('/', methods=['GET'])
@token_required
def get_sessions(user_id):
    sessions = CareerSession.query.filter_by(user_id=user_id).all()
    return sessions_schema.jsonify(sessions), 200

# GET /sessions/<id>
@sessions_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_session(user_id, id):
    session = db.session.get(CareerSession, id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    if session.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    return session_schema.jsonify(session), 200

# PUT /sessions/<id>
@sessions_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_session(user_id, id):
    session = db.session.get(CareerSession, id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    if session.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    for field in ['focus', 'notes']:
        if field in data:
            setattr(session, field, data[field])
    db.session.commit()
    return session_schema.jsonify(session), 200

# DELETE /sessions/<id>
@sessions_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_session(user_id, id):
    session = db.session.get(CareerSession, id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    if session.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(session)
    db.session.commit()
    return jsonify({'message': 'Session deleted'}), 200

# PUT /sessions/<id>/assign-advisor/<advisor_id>
@sessions_bp.route('/<int:id>/assign-advisor/<int:advisor_id>', methods=['PUT'])
@token_required
def assign_advisor(user_id, id, advisor_id):
    session = db.session.get(CareerSession, id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    advisor = db.session.get(Advisor, advisor_id)
    if not advisor:
        return jsonify({'error': 'Advisor not found'}), 404
    if advisor in session.advisors:
        return jsonify({'error': 'Advisor already assigned'}), 409
    session.advisors.append(advisor)
    db.session.commit()
    return jsonify({'message': 'Advisor assigned'}), 200

# PUT /sessions/<id>/remove-advisor/<advisor_id>
@sessions_bp.route('/<int:id>/remove-advisor/<int:advisor_id>', methods=['PUT'])
@token_required
def remove_advisor(user_id, id, advisor_id):
    session = db.session.get(CareerSession, id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    advisor = db.session.get(Advisor, advisor_id)
    if not advisor:
        return jsonify({'error': 'Advisor not found'}), 404
    if advisor not in session.advisors:
        return jsonify({'error': 'Advisor not assigned'}), 404
    session.advisors.remove(advisor)
    db.session.commit()
    return jsonify({'message': 'Advisor removed'}), 200
