from flask import Flask
from controllers.music_controller import music_bp
from controllers.playlist_controller import playlist_bp
from controllers.user_controller import user_bp
from controllers.home_controller import home_bp
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///muzlik.db'

# Register the blueprint for the music controller
app.register_blueprint(music_bp)
app.register_blueprint(playlist_bp)
app.register_blueprint(user_bp)
app.register_blueprint(home_bp)

# Initialize the database
db.init_app(app)

if __name__ == '__main__':
    app.run()