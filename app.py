import os
import yaml
from flask import Flask, request, render_template, redirect, url_for, flash
from modules.data_reader import make_dir_if_not_exist
from page_object.search_utils import search_data
from page_object.login_utils import validate_creds
from page_object.signup_utils import is_identifier_already_used, is_email_used, is_username_used, add_user_data
from page_object.dashboard_utils import get_user_details
from page_object.edit_details_utils import update_user_details
from modules.image_utils import convert_img_to_binary, get_picture_url_from_binary
from modules.session_manager import get_session
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
    email = request.form['username']
    password = request.form['password']
    _id, is_creds_valid = validate_creds(identifier=email, password=password)
    if is_creds_valid:
        session['logged_in'] = True
        session['user_id'] = _id
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('home'))
    #_id, creds = get_user_creds(email)
    #creds = creds.get('creds')
    #if email == creds.get('Email') or email == creds.get('Phone') or email == creds.get('user_name'):
    #    if password == creds.get('password'):
    #        session['logged_in'] = True
    #        session['creds'] = creds
    #        session['user_id'] = _id
    #        return redirect(url_for('dashboard'))
    #    else:
    #        flash('Invalid credentials. Please try again.', 'danger')
    #        return redirect(url_for('home'))
    #else:
    #    flash('No such email id found. Please signup first', 'danger')
    #    return redirect(url_for('home'))


@app.route('/signup', methods=['POST'])
def signup():
    identifier = request.form['identifier']
    # _id, creds = get_user_creds(identifier)
    # creds = creds.get('creds')
    # if identifier == creds.get('user_name') or identifier == creds.get('Phone') or identifier == creds.get('Email'):
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
    print(f'First Entry {session}')
    if 'logged_in' in session:
        if session.get('logged_in'):
            print(f'User ID {session.get("user_id")}')
            # user_data = get_user_data(session.get('user_id'))
            user_data = get_user_details(session.get('user_id'))
            print(f'After login user_data {user_data.get("Name")}, {user_data.get("UserName")}, {user_data.get("Salt")}')
            return render_template('dashboard.html', **user_data)
    else:
        return redirect(url_for('home'))


@app.route('/edit')
def edit():
    if 'logged_in' in session:
        if session.get('logged_in'):
            # user_data = get_user_data(session.get('user_id'))
            user_data = get_user_details(session.get('user_id'))
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
            picture_binary = get_picture_url_from_binary(convert_img_to_binary(file))
    update_user_details(session.get('user_id'), picture_binary=picture_binary, name=name, gender=gender, phone=phone, email=email, address_l1=address_l1, address_l2=address_l2, dob=dob, city=city, state=state, country=country)
    # update_data(session.get('user_id'), picture_binary=picture_binary, name=name, gender=gender, phone=phone, email=email, address_l1=address_l1, address_l2=address_l2, dob=dob, city=city, state=state, country=country)
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
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
