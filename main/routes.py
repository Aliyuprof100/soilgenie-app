from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Welcome')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'agent':
        # Logic for agent dashboard will go here
        return render_template('main/agent_dashboard.html', title='Agent Dashboard')
    elif current_user.role == 'farmer':
        # Logic for farmer dashboard will go here
        farms = [] # Placeholder
        weather = None # Placeholder
        return render_template('main/farmer_dashboard.html', title='My Dashboard', farms=farms, weather=weather)
    else:
        return "Error: Unknown user role.", 403