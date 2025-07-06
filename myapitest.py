from flask import Flask, request, jsonify, Response
from classes.mycar import Car
import json
from functools import wraps

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def Hello():
    return jsonify({"message" : "Merhaba, Flask API'nize hoş geldiniz! Kullanabileceğiniz endpointler: POST /api/car  GET /api/araba"})

araba = []
@app.route('/api/car', methods=['POST'])
def handle_car_request2():
    data = request.json
    try:
        make = data.get('make')
        model = data.get('model')
        year = data.get('year')
        if not all([make, model, year]):
            return jsonify({"error": "Gerekli alanlar eksik"}), 400
        araba.append(data)
        car = Car(make, model, year)
        return jsonify({'car': car.__dict__}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/araba', methods=['GET'])
def get_araba():
    if not araba:
        return jsonify({"message": "Araba bulunamadı"}), 404
    return jsonify({"cars": araba}), 200

if __name__ == '__main__':
    app.run(debug=True)
