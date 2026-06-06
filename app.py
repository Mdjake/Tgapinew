from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ORIGINAL_API_URL = "http://Api.subhxcosmo.in/api"
ORIGINAL_API_KEY = os.environ.get("API_KEY", "KRISHRDP2")

@app.route('/')
def index():
    return jsonify({"status": "running", "usage": "/api?type=...&term=..."})

@app.route('/api', strict_slashes=False)
def proxy():
    req_type = request.args.get('type')
    term = request.args.get('term')

    if not req_type or not term:
        return jsonify({"error": "Missing type or term parameter"}), 400

    params = {
        'key': ORIGINAL_API_KEY,
        'type': req_type,
        'term': term
    }

    try:
        response = requests.get(ORIGINAL_API_URL, params=params, timeout=15)
        data = response.json()
    except Exception as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500

    if data.get('success') and 'result' in data:
        result = data['result']
        if not result.get('success'):
            return jsonify({"error": result.get('msg', 'Not found')}), 404

        return jsonify({
            "developer": "helper man",
            "data": {
                "country_code": result.get('country_code'),
                "number": result.get('number')
            }
        })
    else:
        return jsonify({"error": data.get('message', 'Invalid response from original API')}), 500
