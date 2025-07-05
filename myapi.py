from flask import Flask, jsonify, request, Response
from classes.mycar import Car
import json
from functools import wraps



app = Flask(__name__)

@app.route('/api', methods=['GET'])
def Hello():
    return jsonify({"message": "Hello, from your flask API!"})


@app.route('/api/car', methods=['POST'])
def handle_car_request():
    data = request.json
    try:
        make = data.get('make')
        model = data.get('model')
        year = data.get('year')
        if not all([make, model, year]):
            return jsonify({"error": "Missing required fields"}), 400
        
        car = Car(make, model, year)
        return jsonify({'car': car.__dict__}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

###
# AUTHENTICATION LOGIC
###

VALID_USERNAME = "admin"
VALID_PASSWORD = "secret"

def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return username == VALID_USERNAME and password == VALID_PASSWORD

def authenticate():
    """Sends a 401 response that enables basic auth."""
    return Response(
        'Could not verify!', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    """Decorator to prompt for authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
@requires_auth
def protected():
    """A protected route that requires authentication."""
    return jsonify({"message": "This is a protected route!"})

####
# Stop Auth logic
####


if __name__ == '__main__':
    app.run(debug=True)