from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from utils import hash_password, check_password
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    d = request.get_json()

    if User.query.filter_by(username=d['username']).first():
        return jsonify({'msg': 'User already exists'}), 400

    user = User(
        username=d['username'],
        email=d['email'],
        password_hash=hash_password(d['password'])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'access_token': create_access_token(identity=str(user.id))
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    d = request.get_json()
    user = User.query.filter_by(username=d['username']).first()

    if not user or not check_password(d['password'], user.password_hash):
        return jsonify({'msg': 'Invalid credentials'}), 401

    return jsonify({
        'access_token': create_access_token(identity=str(user.id))
    })
