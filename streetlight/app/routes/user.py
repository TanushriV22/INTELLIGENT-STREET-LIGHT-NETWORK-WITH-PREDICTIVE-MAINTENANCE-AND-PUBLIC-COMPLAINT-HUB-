from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.complaint import Complaint

user = Blueprint('user', __name__)

@user.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    complaints = Complaint.get_user_complaints(current_user.id)
    return render_template('user/dashboard.html', complaints=complaints)

@user.route('/submit-complaint', methods=['GET', 'POST'])
@login_required
def submit_complaint():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        location = request.form.get('location')
        description = request.form.get('description')
        
        # Validate inputs
        if not location or not description:
            flash('All fields are required.', 'danger')
            return render_template('user/submit_complaint.html')
        
        # Create new complaint
        complaint = Complaint.create_complaint(current_user.id, location, description)
        if complaint:
            flash('Complaint submitted successfully!', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash('Failed to submit complaint. Please try again.', 'danger')
    
    return render_template('user/submit_complaint.html')

@user.route('/view-complaint/<int:complaint_id>')
@login_required
def view_complaint(complaint_id):
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    complaint = Complaint.get_complaint_by_id(complaint_id)
    
    if not complaint or complaint.user_id != current_user.id:
        flash('Complaint not found or you do not have permission to view it.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/view_complaint.html', complaint=complaint)
