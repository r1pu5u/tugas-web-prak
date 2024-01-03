from flask import Flask, render_template, request, jsonify
from music_routes import uplad


from models.db import User, db, Music, Playlist
from controllers import MusicControlerer
# app.register_blueprint(uplad, url_prefix='/music')
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')



@app.route("/testing")
def testing():
    return render_template('testing.html')

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
    
@app.route("/api/music/", methods=['POST',  'PUT'])
@app.route('/api/music/<int:music_id>', methods=['GET', 'DELETE'])
def upload_music(music_id=None):
    music = MusicControlerer(app.root_path, app)
    if request.method == "GET" and music_id != None:
        data = music.get_music_by_id(music_id)
        return data
    elif request.method == "DELETE" and music_id != None:
        data = music.delete_music(music_id)
        return data
    
    title = request.form.get('title')
    artist = request.form.get('artist')
    user_id = request.form.get('user_id')
    lirik = request.form.get('lirik')

    file_music = request.files['file_music']

    file_thumbnail = request.files['file_thumbnail']
    if request.method == "POST":
        music.create_music(title, artist, user_id, lirik, file_music, file_thumbnail)
    

@app.route("/api/playlist/", methods=['POST',  'PUT'])
@app.route('/api/playlist/<int:playlist_id>', methods=['GET', 'DELETE'])
def playlist(playlist_id):
    if request.method == "GET":
        return Playlist.query.get(playlist_id)

    
    data = request.get_json()
    id_music = data.get('id_music')
    created_tgl = data.get('created_tgl')
    created_by = data.get('created_by')


    if request.method == "POST":
        new_playlist = Playlist(id_music=id_music, created_tgl=created_tgl, created_by=created_by)
        db.session.add(new_playlist)
        db.session.commit()
    elif request.method == "PUT":
        playlist = Playlist.query.get(playlist_id)
        playlist.id_music = id_music
        playlist.created_tgl = created_tgl
        playlist.created_by = created_by
        db.session.commit()
    elif request.method == "DELETE":
        playlist = Playlist.query.get(playlist_id)
        db.session.delete(playlist)
        db.session.commit()



if __name__ == "__main__":
    app.run(debug=True)