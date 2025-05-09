from app import create_app, db
from app.models.user import User
from app.models.complaint import Complaint
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Create admin user if not exists
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            name='Admin User',
            email='admin@example.com',
            password=User.hash_password('admin123'),
            is_admin=True,
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        print("Admin user created")
    
    # Create regular user if not exists
    user = User.query.filter_by(email='user@example.com').first()
    if not user:
        user = User(
            name='Test User',
            email='user@example.com',
            password=User.hash_password('user123'),
            is_admin=False,
            created_at=datetime.utcnow()
        )
        db.session.add(user)
        print("Regular user created")
    
    # Create sample complaints if none exist
    if not Complaint.query.first():
        # Create a few sample complaints for the regular user
        complaint1 = Complaint(
            user_id=2,  # This assumes the regular user has ID 2
            location='Main Street, Corner of 5th Avenue',
            description='Streetlight is flickering at night',
            status='pending',
            created_at=datetime.utcnow()
        )
        
        complaint2 = Complaint(
            user_id=2,  # This assumes the regular user has ID 2
            location='Park Avenue, Near Central Park',
            description='Streetlight is completely out',
            status='in_progress',
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        
        complaint3 = Complaint(
            user_id=2,  # This assumes the regular user has ID 2
            location='Broadway and 42nd Street',
            description='Streetlight pole is damaged and leaning',
            status='resolved',
            created_at=datetime.utcnow() - timedelta(days=5)
        )
        
        db.session.add_all([complaint1, complaint2, complaint3])
        print("Sample complaints created")
    
    db.session.commit()
    print("Database setup complete!")
