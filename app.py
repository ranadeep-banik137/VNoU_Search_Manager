import os
import yaml
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from modules.data_reader import make_dir_if_not_exist
from page_object.search_utils import search_data
from page_object.user_details import get_user_data, update_data, get_user_creds, add_data
from modules.image_utils import convert_img_to_binary
from modules.session_manager import add_session, get_session, clear_session
from flask_session import Session
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
app.config['SESSION_TYPE'] = 'filesystem'  # Or use 'redis' or 'sqlalchemy'
Session(app)
session = get_session()


@app.route('/')
def home():
    if 'logged_in' in session:
        if session.get('logged_in'):
            return redirect(url_for('dashboard'))
    return render_template('full.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    _id, creds = get_user_creds(email)
    creds = creds.get('creds')
    if email == creds.get('Email') or email == creds.get('Phone') or email == creds.get('user_name'):
        if password == creds.get('password'):
            session['logged_in'] = True
            session['creds'] = creds
            session['user_id'] = _id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('home'))
    else:
        flash('No such email id found. Please signup first', 'danger')
        return redirect(url_for('home'))


@app.route('/signup', methods=['POST'])
def signup():
    if 'logged_in' in session:
        if session.get('logged_in'):
            flash('User session already exist. Please sign out first', 'danger')
    identifier = request.form['identifier']
    _id, creds = get_user_creds(identifier)
    creds = creds.get('creds')
    if identifier == creds.get('user_name') or identifier == creds.get('Phone') or identifier == creds.get('Email'):
        flash('User already exists', 'danger')
        return redirect(url_for('home'))
    else:
        # Code to handle new user signup
        flash('Signup successful!', 'success')
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
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    identifier = email  # or phone or username depending on your logic
    _id, creds = get_user_creds(identifier)
    if identifier == creds.get('Email'):
        flash('User already exists', 'danger')
        return redirect(url_for('index'))

    # Save the profile picture
    profile_picture = request.files['profile_picture']
    print(f'picture found {profile_picture}')
    profile_picture_binary = None
    if profile_picture:
        filename = secure_filename(profile_picture.filename)
        print(f'Filename uploaded: {filename}')
        profile_picture_binary = convert_img_to_binary(profile_picture)
        # profile_picture.save('templates/uploads/', filename)
    if new_password != confirm_password:
        flash('Re-type the passwords. It does not match', 'danger')
        return redirect(url_for('new_user'))
    else:
        add_data(picture_binary=profile_picture_binary, name=full_name, email=email, phone=phone, state=state, city=city, country=country, address_l1=address1, address_l2=address2, dob=dob, gender=gender, new_password=new_password)
        flash('Signup successful!', 'success')
        return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    print(f'First Entry {session}')
    if 'logged_in' in session:
        if session.get('logged_in'):
            print(f'User ID {session.get("user_id")}')
            user_data = get_user_data(session.get('user_id'))
            return render_template('dashboard.html', **user_data)
    else:
        return redirect(url_for('home'))


@app.route('/edit')
def edit():
    if 'logged_in' in session:
        if session.get('logged_in'):
            user_data = get_user_data(session.get('user_id'))
            return render_template('edit_details.html', **user_data)
    else:
        return redirect(url_for('home'))


@app.route('/update_details', methods=['POST'])
def update_details():
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    data = request.form
    print(f'Received form data {data}')
    print(f'Profile pic in files: {request.files}')
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
    picture_binary = None
    if 'profile_picture' not in request.files:
        flash(f'No file part {"but image was uploaded" if image_edited else "as no image uploaded"}')
    if image_edited and 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and file.filename:
            picture_binary = convert_img_to_binary(file)
    update_data(session.get('user_id'), picture_binary=picture_binary, name=name, gender=gender, phone=phone, email=email, address_l1=address_l1, address_l2=address_l2, dob=dob, city=city, state=state, country=country)
    flash('Data updated successfully!', 'success')
    return redirect(url_for('edit'))


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
