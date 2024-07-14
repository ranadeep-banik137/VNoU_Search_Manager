from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from modules.json_filtering import filter_jsons_by_attrs
from modules.data_reader import get_json_objects_from_directory, get_active_attributes

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management


# Dummy function to represent your search function
def search_data(name=None, detection_time=None, frame_number=None, user_id=None, email=None, has_saved_image=False, unidentified_reason=None):
    # This should be replaced with your actual search function logic
    attr_values = get_active_attributes(name, detection_time, frame_number, user_id, email, has_saved_image, unidentified_reason)
    print(f'Attrs {attr_values}')
    file_dest = 'files/json_reports'
    all_jsons = get_json_objects_from_directory(file_dest)
    results = filter_jsons_by_attrs(all_jsons, attr_values)
    print(f'Results {results}')
    return results


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    data = request.form
    name = data.get('name') or None
    detection_time = data.get('detection_time') or None
    frame_number = data.get('frame_number')
    user_id = data.get('user_id')
    email = data.get('email') or None
    has_saved_image = data.get('has_saved_image')
    unidentified_reason = data.get('unidentified_reason') or None

    # Convert numeric fields to int if they are provided
    frame_number = int(frame_number) if frame_number else None
    user_id = int(user_id) if user_id else None
    has_saved_image = has_saved_image.lower() == 'true' if has_saved_image else None

    # Call your search function
    results = search_data(name, detection_time, frame_number, user_id, email, has_saved_image, unidentified_reason)

    # Store the results in session
    session['results'] = results

    return redirect(url_for('results'))


@app.route('/results')
def results():
    results = session.get('results', [])
    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
