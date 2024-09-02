# app.py
from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    start = int(request.form['start'])
    end = int(request.form['end'])
    total_chunks = int(request.form['totalChunks'])

    chunk_filename = 'uploaded_file.mp4'

    with open(os.path.join(UPLOAD_FOLDER, chunk_filename), 'ab') as f:
        f.write(file.read())

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
