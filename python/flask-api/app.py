# ============================================================
# Visible — Career Intelligence REST API
# Relational Databases & API Rest Development Project
# Coding Temple Advanced Python Module
#
# Full Flask REST API using MySQL, SQLAlchemy, and Marshmallow.
# Domain: Visible career intelligence platform.
#
# Tables:
#   VisibleUser        — professionals using the platform
#   ContributionEntry  — documented work contributions
#   PromotionCase      — links users to contribution evidence
#   case_contributions — many-to-many association table
#
# Endpoints:
#   Users:         GET/POST /users, GET/PUT/DELETE /users/<id>
#   Contributions: GET/POST /contributions, GET/PUT/DELETE /contributions/<id>
#   Cases:         POST /cases, GET /cases/user/<id>
#                  PUT /cases/<id>/add_contribution/<contrib_id>
#                  DELETE /cases/<id>/remove_contribution/<contrib_id>
#                  GET /cases/<id>/contributions
# ============================================================

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Table, Column, Integer, ForeignKey
from datetime import datetime, timezone

# ============================================================
# APP CONFIGURATION
# ============================================================

app = Flask(__name__)

# MySQL connection — password loaded from environment variable
# Set before running: $env:MYSQL_PASSWORD = "your_password"
mysql_password = os.environ.get('MYSQL_PASSWORD', 'root')

from urllib.parse import quote_plus
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'sqlite:///visible_api.db'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# ============================================================
# ASSOCIATION TABLE — Many-to-Many
# ============================================================
# A PromotionCase can have many ContributionEntries
# A ContributionEntry can appear in many PromotionCases
# This association table prevents duplicate entries

case_contributions = Table(
    'case_contributions',
    db.metadata,
    Column('case_id',
           Integer,
           ForeignKey('promotion_cases.id'),
           primary_key=True),
    Column('contribution_id',
           Integer,
           ForeignKey('contribution_entries.id'),
           primary_key=True)
)


# ============================================================
# MODELS
# ============================================================

class VisibleUser(db.Model):
    """
    A professional using the Visible platform.
    One user can have many promotion cases.
    """
    __tablename__ = 'visible_users'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    address    = db.Column(db.String(200), nullable=True)
    email      = db.Column(db.String(100), unique=True, nullable=False)
    job_title  = db.Column(db.String(100), nullable=True)
    company    = db.Column(db.String(100), nullable=True)

    # One user → many promotion cases
    cases = db.relationship('PromotionCase', back_populates='user',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<VisibleUser {self.name}>'


class ContributionEntry(db.Model):
    """
    A documented work contribution.
    Can appear in many promotion cases via many-to-many.
    """
    __tablename__ = 'contribution_entries'

    id           = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)  # title
    category     = db.Column(db.String(50), nullable=False)
    price        = db.Column(db.Float, nullable=False)         # impact score
    description  = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<ContributionEntry {self.product_name}>'


class PromotionCase(db.Model):
    """
    A promotion case linking a user to their contribution evidence.
    One user → many cases.
    Many cases ←→ many contributions via association table.
    """
    __tablename__ = 'promotion_cases'

    id         = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc))
    user_id    = db.Column(db.Integer,
                           db.ForeignKey('visible_users.id'),
                           nullable=False)
    # Bonus: shipped = submitted to manager
    submitted  = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship('VisibleUser', back_populates='cases')
    contributions = db.relationship(
        'ContributionEntry',
        secondary=case_contributions,
        backref='cases'
    )

    def __repr__(self):
        return f'<PromotionCase {self.id} user={self.user_id}>'


# ============================================================
# MARSHMALLOW SCHEMAS
# ============================================================

class VisibleUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VisibleUser
        load_instance = True
        include_fk = True


class ContributionEntrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContributionEntry
        load_instance = True
        include_fk = True


class PromotionCaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PromotionCase
        load_instance = True
        include_fk = True


# Schema instances
user_schema         = VisibleUserSchema()
users_schema        = VisibleUserSchema(many=True)
contrib_schema      = ContributionEntrySchema()
contribs_schema     = ContributionEntrySchema(many=True)
case_schema         = PromotionCaseSchema()
cases_schema        = PromotionCaseSchema(many=True)


# ============================================================
# USER ENDPOINTS
# ============================================================

@app.route('/users', methods=['GET'])
def get_users():
    """GET /users — Retrieve all users."""
    users = VisibleUser.query.all()
    return jsonify(users_schema.dump(users)), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """GET /users/<id> — Retrieve a user by ID."""
    user = db.session.get(VisibleUser, user_id)
    if not user:
        return jsonify({'error': f'User {user_id} not found'}), 404
    return jsonify(user_schema.dump(user)), 200


@app.route('/users', methods=['POST'])
def create_user():
    """POST /users — Create a new user."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Check for duplicate email
    existing = VisibleUser.query.filter_by(
        email=data.get('email')
    ).first()
    if existing:
        return jsonify({'error': 'Email already exists'}), 409

    user = VisibleUser(
        name      = data.get('name'),
        address   = data.get('address', ''),
        email     = data.get('email'),
        job_title = data.get('job_title', ''),
        company   = data.get('company', '')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """PUT /users/<id> — Update a user by ID."""
    user = db.session.get(VisibleUser, user_id)
    if not user:
        return jsonify({'error': f'User {user_id} not found'}), 404

    data = request.get_json()
    if data.get('name'):
        user.name = data['name']
    if data.get('address'):
        user.address = data['address']
    if data.get('email'):
        user.email = data['email']
    if data.get('job_title'):
        user.job_title = data['job_title']
    if data.get('company'):
        user.company = data['company']

    db.session.commit()
    return jsonify(user_schema.dump(user)), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """DELETE /users/<id> — Delete a user by ID."""
    user = db.session.get(VisibleUser, user_id)
    if not user:
        return jsonify({'error': f'User {user_id} not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {user_id} deleted'}), 200


# ============================================================
# CONTRIBUTION ENDPOINTS
# ============================================================

@app.route('/contributions', methods=['GET'])
def get_contributions():
    """GET /contributions — Retrieve all contribution entries."""
    contributions = ContributionEntry.query.all()
    return jsonify(contribs_schema.dump(contributions)), 200


@app.route('/contributions/<int:contrib_id>', methods=['GET'])
def get_contribution(contrib_id):
    """GET /contributions/<id> — Retrieve a contribution by ID."""
    contrib = db.session.get(ContributionEntry, contrib_id)
    if not contrib:
        return jsonify({'error': f'Contribution {contrib_id} not found'}), 404
    return jsonify(contrib_schema.dump(contrib)), 200


@app.route('/contributions', methods=['POST'])
def create_contribution():
    """POST /contributions — Create a new contribution entry."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    contrib = ContributionEntry(
        product_name = data.get('product_name'),
        category     = data.get('category', 'process'),
        price        = data.get('price', 0.0),
        description  = data.get('description', '')
    )
    db.session.add(contrib)
    db.session.commit()
    return jsonify(contrib_schema.dump(contrib)), 201


@app.route('/contributions/<int:contrib_id>', methods=['PUT'])
def update_contribution(contrib_id):
    """PUT /contributions/<id> — Update a contribution by ID."""
    contrib = db.session.get(ContributionEntry, contrib_id)
    if not contrib:
        return jsonify({'error': f'Contribution {contrib_id} not found'}), 404

    data = request.get_json()
    if data.get('product_name'):
        contrib.product_name = data['product_name']
    if data.get('category'):
        contrib.category = data['category']
    if data.get('price') is not None:
        contrib.price = data['price']
    if data.get('description'):
        contrib.description = data['description']

    db.session.commit()
    return jsonify(contrib_schema.dump(contrib)), 200


@app.route('/contributions/<int:contrib_id>', methods=['DELETE'])
def delete_contribution(contrib_id):
    """DELETE /contributions/<id> — Delete a contribution by ID."""
    contrib = db.session.get(ContributionEntry, contrib_id)
    if not contrib:
        return jsonify({'error': f'Contribution {contrib_id} not found'}), 404

    db.session.delete(contrib)
    db.session.commit()
    return jsonify({'message': f'Contribution {contrib_id} deleted'}), 200


# ============================================================
# PROMOTION CASE ENDPOINTS
# ============================================================

@app.route('/cases', methods=['POST'])
def create_case():
    """POST /cases — Create a new promotion case for a user."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    user = db.session.get(VisibleUser, data.get('user_id'))
    if not user:
        return jsonify({'error': 'User not found'}), 404

    case = PromotionCase(
        user_id    = data.get('user_id'),
        order_date = datetime.now(timezone.utc),
        submitted  = data.get('submitted', False)
    )
    db.session.add(case)
    db.session.commit()
    return jsonify(case_schema.dump(case)), 201


@app.route('/cases/<int:case_id>/add_contribution/<int:contrib_id>',
           methods=['PUT'])
def add_contribution_to_case(case_id, contrib_id):
    """
    PUT /cases/<case_id>/add_contribution/<contrib_id>
    Add a contribution to a promotion case.
    Prevents duplicate entries.
    """
    case = db.session.get(PromotionCase, case_id)
    if not case:
        return jsonify({'error': f'Case {case_id} not found'}), 404

    contrib = db.session.get(ContributionEntry, contrib_id)
    if not contrib:
        return jsonify({'error': f'Contribution {contrib_id} not found'}), 404

    # Prevent duplicates
    if contrib in case.contributions:
        return jsonify({
            'error': 'Contribution already in this case'
        }), 409

    case.contributions.append(contrib)
    db.session.commit()
    return jsonify({
        'message': f'Contribution {contrib_id} added to case {case_id}',
        'case': case_schema.dump(case)
    }), 200


@app.route('/cases/<int:case_id>/remove_contribution/<int:contrib_id>',
           methods=['DELETE'])
def remove_contribution_from_case(case_id, contrib_id):
    """
    DELETE /cases/<case_id>/remove_contribution/<contrib_id>
    Remove a contribution from a promotion case.
    """
    case = db.session.get(PromotionCase, case_id)
    if not case:
        return jsonify({'error': f'Case {case_id} not found'}), 404

    contrib = db.session.get(ContributionEntry, contrib_id)
    if not contrib:
        return jsonify({'error': f'Contribution {contrib_id} not found'}), 404

    if contrib not in case.contributions:
        return jsonify({
            'error': 'Contribution not in this case'
        }), 404

    case.contributions.remove(contrib)
    db.session.commit()
    return jsonify({
        'message': f'Contribution {contrib_id} removed from case {case_id}'
    }), 200


@app.route('/cases/user/<int:user_id>', methods=['GET'])
def get_cases_for_user(user_id):
    """GET /cases/user/<user_id> — Get all cases for a user."""
    user = db.session.get(VisibleUser, user_id)
    if not user:
        return jsonify({'error': f'User {user_id} not found'}), 404

    cases = PromotionCase.query.filter_by(user_id=user_id).all()
    return jsonify(cases_schema.dump(cases)), 200


@app.route('/cases/<int:case_id>/contributions', methods=['GET'])
def get_contributions_for_case(case_id):
    """GET /cases/<case_id>/contributions — Get all contributions in a case."""
    case = db.session.get(PromotionCase, case_id)
    if not case:
        return jsonify({'error': f'Case {case_id} not found'}), 404

    return jsonify(contribs_schema.dump(case.contributions)), 200


# ============================================================
# BONUS: UNSUBMITTED CASES
# ============================================================

@app.route('/cases/unsubmitted', methods=['GET'])
def get_unsubmitted_cases():
    """
    GET /cases/unsubmitted
    Bonus: Get all cases not yet submitted to manager.
    """
    cases = PromotionCase.query.filter_by(submitted=False).all()
    return jsonify(cases_schema.dump(cases)), 200


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

@app.route('/init', methods=['POST'])
def init_db():
    """POST /init — Create all tables and seed sample data."""
    db.create_all()

    # Seed sample data if tables are empty
    if VisibleUser.query.count() == 0:
        # Sample users
        u1 = VisibleUser(
            name='Kathy Matos',
            address='Chicago, IL',
            email='kmatosli@yahoo.com',
            job_title='Senior Operations Analyst',
            company='Acme Financial'
        )
        u2 = VisibleUser(
            name='Jordan Rivera',
            address='New York, NY',
            email='jrivera@gmail.com',
            job_title='Finance Associate',
            company='Meridian Capital'
        )
        db.session.add_all([u1, u2])

        # Sample contributions
        c1 = ContributionEntry(
            product_name='Automated monthly reconciliation — saved 12hrs/mo',
            category='process',
            price=88.5,
            description='Eliminated manual reconciliation process saving '
                        '12 hours per month. Documented before/after metrics.'
        )
        c2 = ContributionEntry(
            product_name='Closed Q3 enterprise deal — $2.4M ARR',
            category='revenue',
            price=96.0,
            description='Led end-to-end sales process for enterprise client. '
                        'Largest deal in company history for this segment.'
        )
        c3 = ContributionEntry(
            product_name='Onboarded and mentored 3 new analysts',
            category='leadership',
            price=74.0,
            description='Designed onboarding curriculum and mentored 3 '
                        'new analysts through their first 90 days.'
        )
        db.session.add_all([c1, c2, c3])
        db.session.commit()

        # Sample cases
        case1 = PromotionCase(user_id=u1.id, submitted=True)
        case2 = PromotionCase(user_id=u2.id, submitted=False)
        db.session.add_all([case1, case2])
        db.session.commit()

        # Add contributions to cases
        case1.contributions.append(c1)
        case1.contributions.append(c3)
        case2.contributions.append(c2)
        db.session.commit()

    return jsonify({
        'message': 'Database initialized',
        'tables': ['visible_users', 'contribution_entries',
                   'promotion_cases', 'case_contributions']
    }), 200


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tables created in visible_api database.")
        print("Visible Career Intelligence API running.")
        print("Base URL: http://localhost:5000")
        print()
        print("Endpoints:")
        print("  GET    /users")
        print("  POST   /users")
        print("  GET    /users/<id>")
        print("  PUT    /users/<id>")
        print("  DELETE /users/<id>")
        print("  GET    /contributions")
        print("  POST   /contributions")
        print("  GET    /contributions/<id>")
        print("  PUT    /contributions/<id>")
        print("  DELETE /contributions/<id>")
        print("  POST   /cases")
        print("  GET    /cases/user/<user_id>")
        print("  PUT    /cases/<id>/add_contribution/<contrib_id>")
        print("  DELETE /cases/<id>/remove_contribution/<contrib_id>")
        print("  GET    /cases/<id>/contributions")
        print("  GET    /cases/unsubmitted")
        print("  POST   /init  (seed sample data)")
    app.run(debug=True)

