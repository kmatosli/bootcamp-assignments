from app.extensions import db

class Advisor(db.Model):
    __tablename__ = 'advisors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    specialty = db.Column(db.String(100))
    sessions = db.relationship('CareerSession', backref='advisor', lazy=True)

class VisibleUser(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    job_title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    sessions = db.relationship('CareerSession', backref='user', lazy=True)

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500))

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, default=0.0)
    quantity = db.Column(db.Integer, default=0)

class CareerSession(db.Model):
    __tablename__ = 'career_sessions'
    id = db.Column(db.Integer, primary_key=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisors.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notes = db.Column(db.Text)
    scheduled_at = db.Column(db.DateTime)
