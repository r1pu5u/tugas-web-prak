from flask import Blueprint, request, jsonify, render_template
from models import db, Music
import os
import secrets

music_bp = Blueprint('music', __name__)



# Function to generate a random filename
def randomize_filename(filename):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(filename)
    new_filename = random_hex + file_extension
    return new_filename

def checkExtension(musicname, thumbnailname):
    _, music_extension = os.path.splitext(musicname)
    _, thumbnail_extension = os.path.splitext(thumbnailname)

    valid_image = ['.jpg', '.jpeg', '.png', '.gif']
    valid_image = ['.mp3', '.wav', '.aac', '.wma', '.alac', '.aif', '.dsd']

    if thumbnail_extension.lower() in valid_image and music_extension.lower() in valid_image:
        return False
    
    return True

# Create
def create_music(title, artist, user_id, lirik, file_music, file_thumbnail, genre):
    if checkExtension(file_music.filename, file_thumbnail.filename):
        res = {
            "status": "failed",
            "message": "extensi file tidak valid \n pasitkan thumbnail berekstensi '.jpg', '.jpeg', '.png', '.gif' \n dan music berekstensi '.mp3', '.wav', '.aac', '.wma', '.alac', '.aif', '.dsd'"
        }
        return res

    file_music_filename = randomize_filename(file_music.filename)
    file_thumbnail_filename = randomize_filename(file_thumbnail.filename)
    
    new_music = Music(title=title, artist=artist, user_id=user_id, lirik=lirik, file_music=file_music_filename, file_thumbnail=file_thumbnail_filename, genre=genre)
    db.session.add(new_music)
    db.session.commit()
    
    # Save the uploaded files with the randomized names
    file_music.save(os.path.join(os.getcwd(), 'static/uploads/music', file_music_filename))
    file_thumbnail.save(os.path.join(os.getcwd(), 'static/uploads/thumbnails', file_thumbnail_filename))

    res = {
        "status": "ok",
        "message": "music telah berhasil di upload"
    }

    return res

def get_music_by_id(music_id):
    data = Music.query.get(music_id)
    data = {
            "id": data.id,
            "title": data.title,
            "artist": data.artist,
            "user_id": data.user_id,
            "lirik": data.lirik,
            "file_music": data.file_music,
            "file_thumbnail": data.file_music,
            "genre": data.genre
        }
    return data

def get_music():
    data = Music.query.all()
    arr = []

    for val in data:
        new_data = {
            "id": val.id,
            "title": val.title,
            "artist": val.artist,
            "user_id": val.user_id,
            "lirik": val.lirik,
            "file_music": val.file_music,
            "file_thumbnail": val.file_music,
            "genre": val.genre
        }

        arr.append(new_data)
    return arr

# Update
def update_music(music_id, title, artist, lirik, genre):
    music = Music.query.get(music_id)
    music.title = title
    music.artist = artist
    music.lirik = lirik
    music.genre = genre
    
    # if file_music:
    #     file_music_filename = randomize_filename(file_music.filename)
    #     music.file_music = file_music_filename
    #     file_music.save(os.path.join(os.getcwd(), 'uploads/music', file_music_filename))
    
    # if file_thumbnail:
    #     file_thumbnail_filename = randomize_filename(file_thumbnail.filename)
    #     music.file_thumbnail = file_thumbnail_filename
    #     file_thumbnail.save(os.path.join(os.getcwd(), 'uploads/thumbnails', file_thumbnail_filename))
    
    db.session.commit()

# Delete
def delete_music(music_id):
    music = Music.query.get(music_id)
    # Delete the associated files from the filesystem
    os.remove(os.path.join(os.getcwd(), 'static/uploads/music', music.file_music))
    os.remove(os.path.join(os.getcwd(), 'static/uploads/thumbnail', music.file_thumbnail))
    db.session.delete(music)
    db.session.commit()

@music_bp.route('/test', methods=['POST', 'GET'])
def test_connection():
    return render_template('testing.html')


@music_bp.route("/api/music/", methods=['POST', 'GET'])
@music_bp.route('/api/music/<int:music_id>', methods=['GET', 'DELETE', 'PUT'])
def upload_music(music_id=None):
    
    if request.method == "GET" and music_id != None:
        data = get_music_by_id(music_id)
        return data
    elif request.method == "DELETE" and music_id != None:
        data = delete_music(music_id)
        res = {
            "status": "ok",
            "message": "music telah berhasil di hapus"
        }
        return jsonify(res)
    
    if request.method == "GET":
        data = get_music()
        return jsonify(data)
    
    title = request.form.get('title')
    artist = request.form.get('artist')
    user_id = request.form.get('user_id')
    genre = request.form.get('genre')
    lirik = request.form.get('lirik')

    file_music = request.files['file_music']
    file_thumbnail = request.files['file_thumbnail']
    
    if request.method == "POST":
        data = create_music(title, artist, user_id, lirik, file_music, file_thumbnail, genre)
        
        return jsonify(data)
    if request.method == "PUT" and music_id != None:
        update_music(music_id, title, artist, lirik, genre)
        res = {
            "status": "ok",
            "message": "music telah berhasil di ubah"
        }
        return jsonify(res)