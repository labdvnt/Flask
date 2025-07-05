from flask import Flask, jsonify, request, Response


app = Flask(__name__)

people = []

@app.route('/person', methods=['POST'])
def add_person():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    if not name or not age:
        return jsonify({"error": "Missing required fields"}), 400
    person = {"name": name, "age": age}
    people.append(person)
    return jsonify({"message": "Person added successfully", "person": person}), 201

@app.route('/people', methods=['GET'])
def get_people():
    return jsonify({"people": people}), 200

if __name__ == '__main__':
    app.run(debug=True)





