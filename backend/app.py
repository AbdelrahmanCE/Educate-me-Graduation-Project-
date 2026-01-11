from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db, jwt

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'educateme_secret'
    app.config['JWT_SECRET_KEY'] = 'educateme_jwt'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///educateme.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from models import User
    with app.app_context():
        db.create_all()

    from auth import auth_bp
    from upload import upload_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(upload_bp, url_prefix='/api')

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})

    return app

if __name__ == '__main__':
    create_app().run(debug=False, threaded=True)

