import os
import yaml
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from modules.json_filtering import filter_jsons_by_ranges
from modules.data_reader import get_json_objects_from_directory, get_active_attributes
from modules.config_reader import read_config
from modules.data_reader import make_dir_if_not_exist
from flask_session import Session

config = read_config()
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
app.config['SESSION_TYPE'] = 'filesystem'  # Or use 'redis' or 'sqlalchemy'
Session(app)


# Dummy function to represent your search function
def search_data(name=None, start_detection_time=None, end_detection_time=None, start_frame_number=None, end_frame_number=None, user_id=None, email=None, has_saved_image=False, unidentified_reason=None):
    # This should be replaced with your actual search function logic
    attr_values = get_active_attributes(name, start_detection_time, end_detection_time, start_frame_number, end_frame_number, user_id, email, has_saved_image, unidentified_reason)
    print(f'Attrs {attr_values}')
    file_dest = config['file_transfer']['dest']
    all_jsons = get_json_objects_from_directory(file_dest)
    results = filter_jsons_by_ranges(all_jsons, attr_values)
    print(f'Results {results}')
    return results


@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('full.html')


@app.route('/search', methods=['POST'])
def search():
    data = request.form
    print(f'Received form data: {data}')
    name = data.get('name') or None
    start_detection_time = data.get('start_detection_time') or None
    print(f'Start detected at : {start_detection_time}')
    end_detection_time = data.get('end_detection_time') or None
    print(f'End detected at : {end_detection_time}')
    start_frame_number = data.get('start_frame_number')
    end_frame_number = data.get('end_frame_number')
    user_id = data.get('user_id')
    email = data.get('email') or None
    has_saved_image = data.get('has_saved_image')
    unidentified_reason = data.get('unidentified_reason') or None

    # Convert numeric fields to int if they are provided
    start_frame_number = int(start_frame_number) if start_frame_number else None
    end_frame_number = int(end_frame_number) if end_frame_number else None
    user_id = int(user_id) if user_id else None
    has_saved_image = has_saved_image.lower() == 'true' if has_saved_image else None

    # Call your search function
    results = search_data(name, start_detection_time, end_detection_time, start_frame_number, end_frame_number, user_id, email, has_saved_image, unidentified_reason)

    # Store the results in session
    session['results'] = results

    return redirect(url_for('results'))


@app.route('/results')
def results():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    results = session.get('results', [])
    return render_template('results.html', results=results)


@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')


# Hardcoded credentials for login
HARD_CODED_EMAIL = 'test@example.com'
HARD_CODED_PASSWORD = 'password'


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if email == HARD_CODED_EMAIL and password == HARD_CODED_PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('home'))


@app.route('/signup', methods=['POST'])
def signup():
    flash('Signing up failed', 'danger')
    return redirect(url_for('home'))


@app.route('/onboarding')
def onboarding():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    return render_template('onboarding.html')


@app.route('/search_index')
def search_log():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/submit_onboarding', methods=['POST'])
def submit_onboarding():
    if not session.get('logged_in'):
        return redirect(url_for('home'))

    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    phone = request.form['phone']
    email = request.form['email']
    dob = request.form['dob']
    image = request.files['image']
    make_dir_if_not_exist('templates/uploads/')
    # Save the image
    image_path = os.path.join('templates/uploads', image.filename)
    image.save(image_path)

    # Create a YAML file with the details
    details = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'phone': phone,
        'email': email,
        'dob': dob,
        'image_path': image_path
    }

    yaml_path = os.path.join('templates/uploads', 'details.yml')
    with open(yaml_path, 'w') as yaml_file:
        yaml.dump(details, yaml_file)

    flash('Onboarding data submitted successfully!', 'success')
    return redirect(url_for('onboarding'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
