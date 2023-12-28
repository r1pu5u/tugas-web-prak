from flask import Blueprint, request, jsonify
from models import db, Music

music_bp = Blueprint('music', __name__)

@music_bp.route('/upload', methods=['POST'])
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
