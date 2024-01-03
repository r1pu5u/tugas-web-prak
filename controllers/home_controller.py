from flask import Blueprint, request, jsonify, render_template
from models import db, User

home_bp = Blueprint('home', __name__)


@home_bp.route("/")
def index():
    return render_template('index.html')

@home_bp.route("/search")
def search():
    return render_template('search.html')

@home_bp.route("/admin")
def admin():
    return render_template('admin.html')