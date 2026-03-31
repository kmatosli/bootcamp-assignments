from flask import request, jsonify
from app.blueprints.resources import resources_bp
from app.blueprints.resources.schemas import resource_schema, resources_schema
from app.models import Resource, CareerSession
from app.extensions import db, limiter
from app.utils.auth import advisor_token_required, token_required

# GET /resources
@resources_bp.route('/', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return resources_schema.jsonify(resources), 200

# GET /resources/<id>
@resources_bp.route('/<int:id>', methods=['GET'])
def get_resource(id):
    resource = db.session.get(Resource, id)
    if not resource:
        return jsonify({'error': 'Resource not found'}), 404
    return resource_schema.jsonify(resource), 200

# POST /resources
@resources_bp.route('/', methods=['POST'])
@advisor_token_required
@limiter.limit("10 per minute")
def create_resource(advisor_id):
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    resource = Resource(
        name=data['name'],
        category=data.get('category', ''),
        price=data.get('price', 0.0)
    )
    db.session.add(resource)
    db.session.commit()
    return resource_schema.jsonify(resource), 201

# PUT /resources/<id>
@resources_bp.route('/<int:id>', methods=['PUT'])
@advisor_token_required
def update_resource(advisor_id, id):
    resource = db.session.get(Resource, id)
    if not resource:
        return jsonify({'error': 'Resource not found'}), 404
    data = request.get_json()
    for field in ['name', 'category', 'price']:
        if field in data:
            setattr(resource, field, data[field])
    db.session.commit()
    return resource_schema.jsonify(resource), 200

# DELETE /resources/<id>
@resources_bp.route('/<int:id>', methods=['DELETE'])
@advisor_token_required
def delete_resource(advisor_id, id):
    resource = db.session.get(Resource, id)
    if not resource:
        return jsonify({'error': 'Resource not found'}), 404
    db.session.delete(resource)
    db.session.commit()
    return jsonify({'message': 'Resource deleted'}), 200

# PUT /sessions/<id>/add-resource/<resource_id>
@resources_bp.route('/sessions/<int:session_id>/add-resource/<int:resource_id>', methods=['PUT'])
@token_required
def add_resource_to_session(user_id, session_id, resource_id):
    session = db.session.get(CareerSession, session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    resource = db.session.get(Resource, resource_id)
    if not resource:
        return jsonify({'error': 'Resource not found'}), 404
    if resource in session.resources:
        return jsonify({'error': 'Resource already added'}), 409
    session.resources.append(resource)
    db.session.commit()
    return jsonify({'message': 'Resource added to session'}), 200