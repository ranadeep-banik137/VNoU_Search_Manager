import os
import yaml
from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from modules.data_reader import make_dir_if_not_exist
from page_object.search_utils import search_data
from page_object.login_utils import validate_creds
from page_object.signup_utils import is_identifier_already_used, is_email_used, is_username_used, add_user_data
from page_object.dashboard_utils import get_user_details
from page_object.edit_details_utils import update_user_details
from modules.image_utils import convert_img_to_binary, get_picture_url_from_binary
from modules.session_manager import get_session
from modules.database_util import create_table
from constants.database_constants import Create_table_queries
from flask_session import Session
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
app.config['SESSION_TYPE'] = 'filesystem'  # Or use 'redis' or 'sqlalchemy'
Session(app)
session = get_session()


@app.route('/homepage_logo')
def homepage_logo():
    logo_path = os.path.join(app.root_path, 'static', 'images', 'VNOU-LOGO.png')
    # logo_path = os.path.join(app.root_path, 'static', 'images', 'VNOU-Black-BG-RM.png')
    return send_file(logo_path, mimetype='image/png')


@app.route('/inner_page_logo')
def inner_page_logo():
    logo_path = os.path.join(app.root_path, 'static', 'images', 'VNOU-LOGO-BG-RM.png')
    return send_file(logo_path, mimetype='image/png')


@app.route('/')
def home():
    if 'logged_in' in session:
        if session.get('logged_in'):
            return redirect(url_for('dashboard'))
    return render_template('full.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    _id, is_creds_valid = validate_creds(identifier=username, password=password)
    if is_creds_valid:
        session['logged_in'] = True
        session['user_id'] = _id
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('home'))


@app.route('/signup', methods=['POST'])
def signup():
    identifier = request.form['identifier']
    if is_identifier_already_used(identifier=identifier):
        flash('User already exists', 'danger')
        return redirect(url_for('home'))
    else:
        flash('Please provide valid sign up details', 'success')
        return redirect(url_for('new_user'))


@app.route('/new_user')
def new_user():
    return render_template('signup_details.html')


@app.route('/register', methods=['POST'])
def register():
    full_name = request.form['full_name']
    email = request.form['email']
    dob = request.form['dob']
    gender = request.form['gender']
    phone = request.form['phone']
    address1 = request.form['address1']
    address2 = request.form['address2']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    username = request.form['user_name']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    identifier = email  # or phone or username depending on your logic
    if is_email_used(identifier=identifier):
        flash('Email already exists', 'danger')
        return redirect(url_for('new_user'))
    # Save the profile picture
    profile_picture = request.files['profile_picture']
    profile_picture_binary = None
    if profile_picture:
        filename = secure_filename(profile_picture.filename)
        profile_picture_binary = convert_img_to_binary(profile_picture)
        # profile_picture.save('templates/uploads/', filename)
    if new_password != confirm_password:
        flash('Re-type the passwords. It does not match', 'danger')
        return redirect(url_for('new_user'))
    if is_username_used(username):
        flash('Username already exists. Please try again', 'danger')
        return redirect(url_for('new_user'))
    else:
        add_user_data(picture_binary=profile_picture_binary, name=full_name, email=email, phone=phone, state=state, city=city, country=country, address_l1=address1, address_l2=address2, dob=dob, gender=gender, new_password=new_password, username=username)
        flash('Signup successful!', 'success')
        return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        if session.get('logged_in'):
            user_data = get_user_details(session.get('user_id'))
            return render_template('dashboard.html', **user_data)
    else:
        return redirect(url_for('home'))


@app.route('/edit')
def edit():
    if 'logged_in' in session:
        if session.get('logged_in'):
            user_data = get_user_details(session.get('user_id'))
            return render_template('edit_details.html', **user_data)
    else:
        return redirect(url_for('home'))


@app.route('/update_details', methods=['POST'])
def update_details():
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    data = request.form
    name = data.get('name')
    gender = data.get('gender')
    phone = data.get('phone')
    email = data.get('email')
    address_l1 = data.get('address_l1')
    address_l2 = data.get('address_l2')
    dob = data.get('dob')
    city = data.get('city')
    country = data.get('country')
    state = data.get('state')
    image_edited = request.form.get('image_edited') == 'true'
    profile_picture_binary = None
    profile_picture = request.files['profile_picture'] if 'profile_picture' in request.files else None
    if profile_picture and image_edited:
        filename = secure_filename(profile_picture.filename)
        profile_picture_binary = convert_img_to_binary(profile_picture)
    update_user_details(session.get('user_id'), picture_binary=profile_picture_binary, name=name, gender=gender, phone=phone, email=email, address_l1=address_l1, address_l2=address_l2, dob=dob, city=city, state=state, country=country)
    flash('Data updated successfully!', 'success')
    return redirect(url_for('edit'))


@app.route('/search', methods=['POST'])
def search():
    data = request.form
    name = data.get('name') or None
    start_detection_time = data.get('start_detection_time') or None
    end_detection_time = data.get('end_detection_time') or None
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


def get_results(query, page, per_page):
    data = session.get('results')
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end], len(data)


@app.route('/results')
def results():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    results, total_results = get_results(query, page, per_page)
    total_pages = (total_results + per_page - 1) // per_page  # Calculate total pages
    current_page = page
    page_numbers = range(max(1, current_page - 2), min(total_pages, current_page + 2) + 1)

    return render_template('results.html', results=results, total_pages=total_pages, current_page=current_page, page_numbers=page_numbers)



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
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    create_table(Create_table_queries.user_creds)
    create_table(Create_table_queries.dp_table)
    create_table(Create_table_queries.user_records)
    app.run(debug=True)
