from app import db, login_manager
from flask_login import UserMixin
import hashlib
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with complaints
    complaints = db.relationship('Complaint', backref='author', lazy=True, cascade="all, delete-orphan")
    
    @staticmethod
    def hash_password(password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a password against its hash"""
        hashed_provided = User.hash_password(provided_password)
        return stored_password == hashed_provided
    
    @staticmethod
    def create_user(name, email, password):
        """Create a new user in the database"""
        hashed_password = User.hash_password(password)
        
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            is_admin=False
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user
    
    @staticmethod
    def get_user_by_email(email):
        """Get a user by email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_all_users():
        """Get all non-admin users"""
        return User.query.filter_by(is_admin=False).all()
    
    @staticmethod
    def delete_user(user_id):
        """Delete a user by ID"""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
