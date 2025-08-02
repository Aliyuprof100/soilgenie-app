from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import User, Farm, db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services.weather_service import get_weather_for_location
import json
from ..services import sms_sender

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Welcome')


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
        
        farm_owner = User.query.get(user_id)
        if farm_owner:
            sms_sender.send_analysis_sms(
                phone_number=farm_owner.phone_number,
                farm_name=new_farm.farm_name,
                crop_type=new_farm.crop_type,
                recommendation=new_farm.last_analysis_result
            )
            flash('Analysis SMS has been sent to the farmer!', 'info')
        else:
            flash('Could not find farmer to send SMS.', 'danger')

        # Redirect back to the correct dashboard
        if current_user.role == 'agent':
            return redirect(url_for('main.farmer_profile', user_id=user_id))
        else:
            return redirect(url_for('main.dashboard'))

    # For a GET request, just show the page
    farm_owner = User.query.get_or_404(user_id)
    return render_template('main/map_farm.html', title='Map Farm', farm_owner=farm_owner)

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'agent':
        # ... (agent logic remains the same)
        farmers = User.query.filter_by(role='farmer').all()
        return render_template('main/agent_dashboard.html', title='Agent Dashboard', farmers=farmers)
    
    elif current_user.role == 'farmer':
        farms = Farm.query.filter_by(user_id=current_user.id).order_by(Farm.id.desc()).all()
        
        weather_forecast = None
        # Find the most recently mapped farm to get a location for the weather
        if farms:
            latest_farm = farms[0]
            # The geojson is stored as a string, so we need to load it as a dictionary
            geojson_dict = json.loads(latest_farm.geojson_boundary)
            weather_forecast = get_weather_for_location(geojson_dict)

        return render_template('main/farmer_dashboard.html', title='My Dashboard', farms=farms, weather=weather_forecast)
    
    else:
        return "Error: Unknown user role.", 403