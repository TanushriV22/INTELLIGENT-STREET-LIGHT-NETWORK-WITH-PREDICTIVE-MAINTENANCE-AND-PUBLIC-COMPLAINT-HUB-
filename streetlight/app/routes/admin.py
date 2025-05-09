from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.complaint import Complaint
from app.models.user import User

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('user.dashboard'))
    
    complaints = Complaint.get_all_complaints()
    return render_template('admin/dashboard.html', complaints=complaints)

@admin.route('/admin/view-complaint/<int:complaint_id>')
@login_required
def view_complaint(complaint_id):
    if not current_user.is_admin:
        return redirect(url_for('user.dashboard'))
    
    complaint = Complaint.get_complaint_by_id(complaint_id)
    
    if not complaint:
        flash('Complaint not found.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/view_complaint.html', complaint=complaint)

@admin.route('/admin/update-status/<int:complaint_id>', methods=['POST'])
@login_required
def update_status(complaint_id):
    if not current_user.is_admin:
        return redirect(url_for('user.dashboard'))
    
    status = request.form.get('status')
    valid_statuses = ['Pending', 'In Progress', 'Resolved']
    
    if status not in valid_statuses:
        flash('Invalid status.', 'danger')
        return redirect(url_for('admin.view_complaint', complaint_id=complaint_id))
    
    success = Complaint.update_status(complaint_id, status)
    
    if success:
        flash('Complaint status updated successfully!', 'success')
    else:
        flash('Failed to update complaint status.', 'danger')
    
    return redirect(url_for('admin.view_complaint', complaint_id=complaint_id))

@admin.route('/admin/delete-complaint/<int:complaint_id>', methods=['POST'])
@login_required
def delete_complaint(complaint_id):
    if not current_user.is_admin:
        return redirect(url_for('user.dashboard'))
    
    success = Complaint.delete_complaint(complaint_id)
    
    if success:
        flash('Complaint deleted successfully!', 'success')
    else:
        flash('Failed to delete complaint.', 'danger')
    
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/manage-users')
@login_required
def manage_users():
    if not current_user.is_admin:
        return redirect(url_for('user.dashboard'))
    
    users = User.get_all_users()
    return render_template('admin/manage_users.html', users=users)

@admin.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('user.dashboard'))
    
    success = User.delete_user(user_id)
    
    if success:
        flash('User deleted successfully!', 'success')
    else:
        flash('Failed to delete user.', 'danger')
    
    return redirect(url_for('admin.manage_users'))
