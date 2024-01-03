from flask import Blueprint, request, jsonify, render_template
from models import db, Playlist

playlist_bp = Blueprint('playlist', __name__)

def get_playlist_by_id(music_id):
    data = Playlist.query.get(music_id)
    data = {
            "id": data.id,
            "id_music": data.id_music,
            "created_tgl": data.created_tgl,
            "created_by": data.created_by,
        }
    return data

def get_playlist():
    data = Playlist.query.all()
    arr = []

    for val in data:
        new_data = {
            "id": val.id,
            "id_music": val.id_music,
            "created_tgl": val.created_tgl,
            "created_by": val.created_by,
        }

        arr.append(new_data)
    return arr

def create_playlist(id_music, created_tgl, created_by):
    new_playlist = Playlist(id_music=id_music, created_tgl=created_tgl, created_by=created_by)
    db.session.add(new_playlist)
    db.session.commit()

def update_playlist(playlist_id,id_music,created_tgl,created_by):
    playlist = Playlist.query.get(playlist_id)
    playlist.id_music = id_music
    playlist.created_tgl = created_tgl
    playlist.created_by = created_by
    db.session.commit()

# Delete
def delete_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
   
    db.session.delete(playlist)
    db.session.commit()

# Function to generate a random filename
@playlist_bp.route("/api/playlist/", methods=['POST',  'PUT'])
@playlist_bp.route('/api/playlist/<int:playlist_id>', methods=['GET', 'DELETE'])
def playlist(playlist_id=None):
    if request.method == "GET" and playlist_id != None:
        data = Playlist.query.get(playlist_id)
        return jsonify(data)
    
    if request.method == "GET":
        data = Playlist.query.all()
        return jsonify(data)


    data = request.get_json()
    id_music = data.get('id_music')
    created_tgl = data.get('created_tgl')
    created_by = data.get('created_by')


    if request.method == "POST":
        create_playlist(id_music, created_tgl, created_by)
        res = {
            "status": "ok",
            "message": "playlist telah berhasil di buat"
        }
        return jsonify(res)
    elif request.method == "PUT" and playlist_id != None:
        update_playlist(playlist_id,id_music,created_tgl,created_by)
        res = {
            "status": "ok",
            "message": "playlist telah berhasil di ubah"
        }
        return jsonify(res)
    elif request.method == "DELETE" and playlist_id != None:
        delete_playlist(playlist_id)
        res = {
            "status": "ok",
            "message": "playlist telah berhasil di hapus"
        }
        return jsonify(res)