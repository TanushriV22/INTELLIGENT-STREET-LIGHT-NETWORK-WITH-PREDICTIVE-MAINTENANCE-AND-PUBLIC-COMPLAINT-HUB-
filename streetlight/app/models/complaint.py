from app import db
from datetime import datetime

class Complaint(db.Model):
    __tablename__ = 'complaints'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # This will be populated by the relationship defined in the User model
    # author = relationship defined in User model
    
    @property
    def user_name(self):
        return self.author.name if self.author else None
    
    @staticmethod
    def create_complaint(user_id, location, description):
        """Create a new complaint in the database"""
        new_complaint = Complaint(
            user_id=user_id,
            location=location,
            description=description,
            status='pending'
        )
        
        db.session.add(new_complaint)
        db.session.commit()
        
        return new_complaint
    
    @staticmethod
    def get_user_complaints(user_id):
        """Get all complaints for a specific user"""
        return Complaint.query.filter_by(user_id=user_id).order_by(Complaint.created_at.desc()).all()
    
    @staticmethod
    def get_all_complaints():
        """Get all complaints with user information"""
        return Complaint.query.order_by(Complaint.created_at.desc()).all()
    
    @staticmethod
    def get_complaint_by_id(complaint_id):
        """Get a complaint by ID"""
        return Complaint.query.get(complaint_id)
    
    @staticmethod
    def update_status(complaint_id, status):
        """Update the status of a complaint"""
        complaint = Complaint.query.get(complaint_id)
        if complaint:
            complaint.status = status
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def delete_complaint(complaint_id):
        """Delete a complaint by ID"""
        complaint = Complaint.query.get(complaint_id)
        if complaint:
            db.session.delete(complaint)
            db.session.commit()
            return True
        return False
