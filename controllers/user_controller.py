from flask import Blueprint, request, jsonify, render_template
from models import db, User

user_bp = Blueprint('user', __name__)

@user_bp.route("/login", methods=['GET', 'POST'])
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

@user_bp.route("/signup", methods=['GET', 'POST'])
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