import os

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import base64
import hashlib
import hmac
import json

load_dotenv()

app = Flask(__name__)

BASE_URL = os.getenv('BASE_URL')
APP_ID = os.getenv('APP_ID')
APP_VERSION = os.getenv('APP_VERSION')
APP_SECRET = os.getenv('APP_SECRET')

@app.route('/', methods=['GET'])
def home():
    return "Hello, Facebook App!"


def base64_url_decode(input_str):
    """
    Decode base64 string with URL-safe characters.
    """
    padding = '=' * (-len(input_str) % 4)  # Pad the input to make its length a multiple of 4
    return base64.urlsafe_b64decode(input_str + padding)


def parse_signed_request(signed_request, secret):
    """
    Parse and verify the signed request from Facebook.
    """
    encoded_sig, payload = signed_request.split('.', 1)

    # Decode signature and payload
    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    # Validate the signature
    expected_sig = hmac.new(
        key=secret.encode(),
        msg=payload.encode(),
        digestmod=hashlib.sha256
    ).digest()

    if sig != expected_sig:
        err_message = 'Bad Signed JSON signature!'
        app.logger.error(err_message)
        return jsonify(
            {"error": err_message}), 400

    return data


@app.route('/facebook_callback', methods=['POST'])
def facebook_callback():
    signed_request = request.form.get('signed_request')
    print(f'Signed request: {signed_request}')
    if not signed_request:
        return jsonify({'error': 'Missing signed_request'}), 400

    data = parse_signed_request(signed_request, APP_SECRET)
    if data is None:
        return jsonify({'error': 'Invalid signature'}), 400

    user_id = data.get('user_id')

    confirmation_code = 'abc123'
    print(f"Deletion request received, confirmation code is {confirmation_code}")
    print(f'Started data deletion process for user_id => {user_id}')

    # Start data deletion process
    status_url = f'{BASE_URL}/deletion?id={confirmation_code}'

    response_data = {
        'url': status_url,
        'confirmation_code': confirmation_code
    }

    print(response_data)  # Log the incoming data for debugging
    response = jsonify(response_data), 200
    return response


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', app_id=APP_ID, app_version=APP_VERSION)


@app.route('/deletion', methods=['GET'])
def deletion():
    deletion_id = request.args.get('id')
    if deletion_id:
        print(f"Received read request for deletion id => {deletion_id}")
        return render_template('deletion_status.html', deletion_id=deletion_id, status='PENDING')
    else:
        return render_template('error.html', message='Invalid deletion request, missing "id" query param.')


if __name__ == '__main__':
    app.run(port=5000)
