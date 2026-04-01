from flask import request, jsonify
from app.blueprints.inventory import inventory_bp
from app.blueprints.inventory.schemas import inventory_schema, inventories_schema
from app.models import Inventory
from app.extensions import db

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    items = Inventory.query.all()
    return inventories_schema.jsonify(items), 200

@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory_item(id):
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return inventory_schema.jsonify(item), 200

@inventory_bp.route('/', methods=['POST'])
def create_inventory_item():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    item = Inventory(name=data['name'], price=data.get('price', 0.0), quantity=data.get('quantity', 0))
    db.session.add(item)
    db.session.commit()
    return inventory_schema.jsonify(item), 201

@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory_item(id):
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    data = request.get_json()
    for field in ['name', 'price', 'quantity']:
        if field in data:
            setattr(item, field, data[field])
    db.session.commit()
    return inventory_schema.jsonify(item), 200

@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory_item(id):
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 200
