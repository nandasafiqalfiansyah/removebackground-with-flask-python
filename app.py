from flask import Flask
from flask_cors import CORS
from image_processing import process_image

app = Flask(__name__)
CORS(app, resources={r"/process_image": {"origins": "*"}})  # Enable CORS

# Define the endpoint for image processing
app.add_url_rule('/process_image', 'process_image', process_image, methods=['POST'])

app.add_url_rule('/', 'process_image', process_image, methods=['GET'])

# Enable auto-reload for development (optional, use it only in development)
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

# nanda safiq alfiansyah
