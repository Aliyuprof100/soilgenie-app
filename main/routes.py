from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import User, Farm, db
from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Welcome')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'agent':
        # An agent's dashboard shows a list of farmers they've registered.
        # For the dual-role model, we assume an agent registers farmers 'under them'.
        # Since our model simplifies this, we will just show a list of all farmers for now.
        # In a future version, we would add an 'agent_id' to the User model.
        farmers = User.query.filter_by(role='farmer').all() # Simplified for now
        return render_template('main/agent_dashboard.html', title='Agent Dashboard', farmers=farmers)
    
    elif current_user.role == 'farmer':
        # A farmer's dashboard shows a list of their own farms.
        farms = Farm.query.filter_by(user_id=current_user.id).all()
        
        # We will add weather logic here later
        weather = None 
        
        return render_template('main/farmer_dashboard.html', title='My Dashboard', farms=farms, weather=weather)
    
    else:
        return "Error: Unknown user role.", 403

@main.route('/farmer/<int:user_id>')
@login_required
def farmer_profile(user_id):
    # Ensure only agents can view other profiles
    if current_user.role != 'agent':
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    farmer = User.query.get_or_404(user_id)
    if farmer.role != 'farmer':
        flash('This user is not a farmer.', 'warning')
        return redirect(url_for('main.dashboard'))
        
    farms = Farm.query.filter_by(user_id=farmer.id).all()
    return render_template('main/farmer_profile.html', title=f"{farmer.name}'s Profile", farmer=farmer, farms=farms)


import random
def run_smarter_ai_simulation(crop_type):
    if crop_type == 'maize':
        return "Soil is likely low on Nitrogen. A high-nitrogen fertilizer like Urea is recommended for best maize yield."
    elif crop_type == 'cassava':
        return "Soil may need more Potassium. An NPK fertilizer with a high 'K' value (e.g., 15-15-20) is advised."
    elif crop_type == 'tomato':
        return "Soil pH could be slightly acidic. Consider applying agricultural lime a few weeks before planting tomatoes."
    else:
        return "Vegetation appears healthy. A balanced NPK 15-15-15 fertilizer is suitable for general maintenance."

@main.route('/map_farm/<int:user_id>', methods=['GET', 'POST'])
@login_required
def map_farm(user_id):
    # Security check: Either you are the farmer, or you are an agent.
    if current_user.id != user_id and current_user.role != 'agent':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        # Get the data from the form
        farm_name = request.form.get('farm_name')
        geojson = request.form.get('geojson_boundary')
        crop_type = request.form.get('crop_type')
        
        if not geojson:
            flash('Please draw the farm boundary on the map.', 'danger')
            return redirect(url_for('main.map_farm', user_id=user_id))

        # Run our simulated AI analysis
        recommendation = run_smarter_ai_simulation(crop_type)

        # Create and save the new farm record
        new_farm = Farm(
            farm_name=farm_name,
            geojson_boundary=geojson,
            crop_type=crop_type,
            last_analysis_result=recommendation,
            user_id=user_id # Link it to the correct owner
        )
        db.session.add(new_farm)
        db.session.commit()
        
        flash(f"Analysis for '{farm_name}' is complete!", 'success')

        # We will add the SMS logic here in the next milestone

        # Redirect back to the correct dashboard
        if current_user.role == 'agent':
            return redirect(url_for('main.farmer_profile', user_id=user_id))
        else:
            return redirect(url_for('main.dashboard'))

    # For a GET request, just show the page
    farm_owner = User.query.get_or_404(user_id)
    return render_template('main/map_farm.html', title='Map Farm', farm_owner=farm_owner)