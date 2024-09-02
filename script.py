from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS to allow requests from your frontend origin
CORS(app, resources={r"/*": {"origins": "https://file-upload-demo.netlify.app"}}, supports_credentials=True)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['OPTIONS', 'POST'])  # Handle both OPTIONS and POST requests
def upload_file():
    if request.method == 'OPTIONS':
        return _build_cors_prelight_response()  # Respond to preflight requests

    file = request.files['file']
    start = int(request.form['start'])
    end = int(request.form['end'])
    total_chunks = int(request.form['totalChunks'])

    chunk_filename = 'uploaded_file.mp4'

    with open(os.path.join(UPLOAD_FOLDER, chunk_filename), 'ab') as f:
        f.write(file.read())

    return jsonify({'status': 'success'}), 200

def _build_cors_prelight_response():
    response = jsonify({'status': 'Preflight request passed'})
    response.headers.add('Access-Control-Allow-Origin', 'https://file-upload-demo.netlify.app')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.after_request
def add_cors_headers(response):
    # Add CORS headers to every response
    response.headers.add('Access-Control-Allow-Origin', 'https://file-upload-demo.netlify.app')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
