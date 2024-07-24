import os
import yaml
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from modules.data_reader import make_dir_if_not_exist
from page_object.search_utils import search_data
from page_object.user_details import get_user_data, update_data
from modules.image_utils import convert_img_to_binary
from flask_session import Session


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
app.config['SESSION_TYPE'] = 'filesystem'  # Or use 'redis' or 'sqlalchemy'
Session(app)


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
    print(f'Start detected at: {start_detection_time}')
    end_detection_time = data.get('end_detection_time') or None
    print(f'End detected at: {end_detection_time}')
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
    user_data = get_user_data(1)
    return render_template('dashboard.html', **user_data)


# Hardcoded credentials for login
HARD_CODED_EMAIL = 'ranadeep.banik@vnousolutions.com'
HARD_CODED_PASSWORD = 'rana#123'


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


@app.route('/update_details', methods=['POST'])
def update_details():
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    data = request.form
    print(f'Received form data {data}')
    print(f'Profile pic in files: {request.files}')
    name = data.get('name')
    gender = ''
    phone = data.get('phone')
    email = data.get('email')
    address_l1 = data.get('address_l1')
    address_l2 = data.get('address_l2')
    dob = data.get('dob')
    city = data.get('city')
    country = data.get('country')
    state = data.get('state')
    image_edited = request.form.get('image_edited') == 'true'
    picture_binary = None
    if 'profile_picture' not in request.files:
        flash(f'No file part {"but image was uploaded" if image_edited else "as no image uploaded"}')
    if image_edited and 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and file.filename:
            picture_binary = convert_img_to_binary(file)
    update_data(1, picture_binary=picture_binary, name=name, gender=gender, phone=phone, email=email, address_l1=address_l1, address_l2=address_l2, dob=dob, city=city, state=state, country=country)
    flash('Data updated successfully!', 'success')
    return redirect(url_for('edit'))


@app.route('/edit')
def edit():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    user_data = get_user_data(1)
    return render_template('edit_details.html', **user_data)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
