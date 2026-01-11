from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from nlp_processor import process_pdf_file
import os

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload-pdf', methods=['POST'])
@jwt_required()
def upload_pdf():
    file = request.files['file']
    os.makedirs('uploads', exist_ok=True)
    path = os.path.join('uploads', file.filename)
    file.save(path)
    return jsonify(process_pdf_file(path))
