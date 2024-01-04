from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///muzlik.db'  # Replace 'your_database_name.db' with your database name
db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    # You can add more fields as needed

    def __repr__(self):
        return f"<User {self.username}>"



class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lirik = db.Column(db.Text, nullable=False)
    file_music = db.Column(db.String(100), nullable=False)
    file_thumbnail = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), db.ForeignKey('genre.genre'), nullable=False)

    def __repr__(self):
        return f"<Music {self.title} by {self.artist}>"
    
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_music = db.Column(db.String(255), nullable=False)
    created_tgl = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
        return f"<Music {self.id} by {self.created_by}>"
    
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f"<Music {self.id} by {self.created_by}>"
    
with app.app_context():
    db.create_all()