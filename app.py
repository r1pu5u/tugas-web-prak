from flask import Flask, render_template, request, jsonify
from music_routes import uplad
app = Flask(__name__)

from models.db import User, db, Music
# app.register_blueprint(uplad, url_prefix='/music')


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        # Find the user in the database
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:  # Note: In a real scenario, you should use a secure method like hashing for password verification
            return jsonify({'message': 'Login successful!'}), 200  # OK status code
        else:
            return jsonify({'message': 'Invalid credentials'}), 401  # Unauthorized status code

    elif request.method == "GET":
        return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phone_number = data.get('phone_number')

        # Check if user already exists
        existing_user = User.query.filter((User.email == email) | (User.username == username) | (User.phone_number == phone_number)).first()

        if existing_user:
            return jsonify({'message': 'User already exists!'}), 409  # Conflict status code

        # Create new user
        new_user = User(username=username, email=email, password=password, phone_number=phone_number)
        
        # Add user to database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully!'}), 201  # Created status code
    
@app.route('/upload', methods=['POST'])
def upload_music():
    title = request.form.get('title')
    artist = request.form.get('artist')
    user_id = request.form.get('user_id')
    file_music = request.files['file_music']
    file_thumbnail = request.files['file_thumbnail']

    # Check if all required fields are present
    if not all([title, artist, user_id, file_music, file_thumbnail]):
        return jsonify({'error': 'Missing data'}), 400

    # Save files to a specific directory (you might want to change this path)
    music_path = f"uploads/music/{file_music.filename}"
    thumbnail_path = f"uploads/thumbnails/{file_thumbnail.filename}"
    file_music.save(music_path)
    file_thumbnail.save(thumbnail_path)

    # Create a new music object and add it to the database
    new_music = Music(
        title=title,
        artist=artist,
        user_id=user_id,
        file_music=music_path,
        file_thumbnail=thumbnail_path
    )

    db.session.add(new_music)
    db.session.commit()

    return jsonify({'message': 'Music uploaded successfully'}), 200




if __name__ == "__main__":
    app.run(debug=True)