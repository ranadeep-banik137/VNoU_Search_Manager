import datetime
import os
from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from page_object.search_utils import search_data
from page_object.login_utils import validate_creds
from page_object.signup_utils import is_identifier_already_used, is_email_used, is_username_used, add_user_data
from page_object.dashboard_utils import get_user_details
from page_object.edit_details_utils import update_user_details
from page_object.onboarding_utils import onboard_users
from page_object.customer_utils import get_all_customer_data, delete_customer_by_id, update_customer_details
from page_object.change_password_utils import validate_email_and_get_id, validate_dob_and_name, validate_username, is_password_existing, update_new_password_for_user
from modules.image_utils import convert_img_to_binary
from modules.session_manager import get_session
from modules.database_util import create_table
from modules.timestamp_util import convert_to_epoch_time, convert_human_readable_date_from_epoch
from constants.database_constants import Create_table_queries, User_creds
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


@app.route('/upload_img')
def upload_img():
    img_path = os.path.join(app.root_path, 'static', 'images', 'Upload DP.png')
    # logo_path = os.path.join(app.root_path, 'static', 'images', 'VNOU-Black-BG-RM.png')
    return send_file(img_path, mimetype='image/png')


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
    print(profile_picture)
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
            member_since = convert_human_readable_date_from_epoch(convert_to_epoch_time(user_data.get(User_creds.created_on)))
            return render_template('dashboard.html', **user_data, member_since=member_since)
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
    user_id = session.get('user_id')
    # make_dir_if_not_exist('templates/uploads/')
    # Save the image
    # image_path = os.path.join('templates/uploads', image.filename)
    # image.save(image_path)

    # Create a YAML file with the details
    details = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'phone': phone,
        'email': email,
        'dob': dob
    }

    message, status = onboard_users(user_id, details, image)

    # yaml_path = os.path.join('templates/uploads', 'details.yml')
    # with open(yaml_path, 'w') as yaml_file:
    #    yaml.dump(details, yaml_file)

    flash(message, status)
    return redirect(url_for('onboarding'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    step = 'email'
    validation_message = None
    validation_status = None
    if request.method == 'POST':
        if 'email' in request.form:
            email = request.form['email']
            user_id, is_email_valid = validate_email_and_get_id(email)
            session['change_password_email_validated'] = is_email_valid
            session['change_password_user_id'] = user_id
            if is_email_valid:
                step = 'dob_fullname'
                validation_message = 'Email validated successfully'
                validation_status = 'success'
            else:
                validation_message = 'Invalid email address'
                validation_status = 'error'

        elif 'dob' in request.form and 'fullname' in request.form:
            dob = request.form['dob']
            fullname = request.form['fullname']
            if validate_dob_and_name(user_id=session.get('change_password_user_id'), dob=dob, name=fullname):
                session['change_password_name_dob_validated'] = True
                return redirect(url_for('set_new_password'))
            else:
                validation_message = 'Invalid DOB or Full Name'
                validation_status = 'error'
                step = 'email'  # Restart the process from the beginning
    return render_template('forgot_password.html', step=step, validation_message=validation_message, validation_status=validation_status)


@app.route('/set_new_password', methods=['GET', 'POST'])
def set_new_password():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    elif session.get('change_password_email_validated') and session.get('change_password_name_dob_validated'):
        pass
    else:
        return redirect(url_for('forgot_password'))
    # Your logic for setting a new password goes here
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Check if the username exists
        if not validate_username(user_id=session.get('change_password_user_id'), username=username):
            return render_template('set_new_password.html', message='Username not found. Re-Type the username')

        if new_password == confirm_password:
            if is_password_existing(search_id=session.get('change_password_user_id'), password=new_password):
                return render_template('set_new_password.html', message='You cannot update your old passwords anymore. Try a new password')
            # Perform the password change logic
            # For example, update the password in the database
            # db.session.query(User).filter_by(username=username).update({"password": new_password})
            update_new_password_for_user(userid=session.get('change_password_user_id'), password=new_password)
            flash('Password updated successfully!', 'success')
            session.clear()
            return redirect(url_for('home', message='Password changed successfully'))
        else:
            return render_template('set_new_password.html', message='Passwords do not match. Re-Type the passwords again')

    return render_template('set_new_password.html')


@app.route('/cust_portal')
def customer_details():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    customers = get_all_customer_data()
    return render_template('customer_details.html', customers=customers)


@app.route('/remove_customer/<customer_id>', methods=['GET', 'POST'])
def remove_customer(customer_id):
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    if not session.get('logged_in'):
        return redirect(url_for('home'))

    # Call a function to remove the customer from the database
    user_id = session.get('user_id')
    result, err = delete_customer_by_id(customer_id=customer_id, user_id=user_id)
    flash(f'Customer {customer_id} removed successfully' if result else err, 'success' if result else 'danger')
    # Redirect back to the customer portal after deletion
    return redirect(url_for('customer_details'))


@app.route('/update_customer')
def update_customers():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    return render_template('edit_cust_details.html')


@app.route('/edit_customer/<customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    user_id = session.get('user_id')
    if request.method == 'POST':
        # Handle POST request to update customer data
        data = request.form
        name = data.get('name')
        contact = data.get('contact')
        email = data.get('email')
        address = data.get('address')
        dob = data.get('dob')
        city = data.get('city')
        country = data.get('country')
        state = data.get('state')
        image_edited = request.form.get('image_edited') == 'true'
        profile_picture_binary = None
        profile_picture = request.files['profile_picture'] if 'profile_picture' in request.files else None
        if profile_picture and image_edited:
            # filename = secure_filename(profile_picture.filename)
            profile_picture_binary = convert_img_to_binary(profile_picture)
        status, err = update_customer_details(customer_id=customer_id, user_id=user_id, img=profile_picture_binary, name=name, contact=contact, email=email, address=address, dob=dob, city=city, state=state, country=country)
        flash(f'Customer data for {name} is updated successfully!' if status else err, 'success' if status else 'danger')

    customer_data = get_all_customer_data(customer_id=customer_id)[0]
    return render_template('edit_cust_details.html', customer_id=customer_id, **customer_data)


if __name__ == '__main__':
    create_table(Create_table_queries.user_creds)
    create_table(Create_table_queries.dp_table)
    create_table(Create_table_queries.user_records)
    create_table(Create_table_queries.roles)
    create_table(Create_table_queries.user_creds_history)
    create_table(Create_table_queries.identifiers)
    create_table(Create_table_queries.identifier_records)
    create_table(Create_table_queries.deleted_identifiers)
    app.run(debug=True)
