from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)

# Veritabanı modeli
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Person {self.name} {self.surname}>'

# Yardımcı fonksiyonlar
def create_response(data, status_code):
    return jsonify(data), status_code

# --- Kimlik Doğrulama Mantığı ---
VALID_USERNAME = "admin"
VALID_PASSWORD = "secret"

def check_auth(username, password):
    """Kullanıcı adı ve parolanın geçerli olup olmadığını kontrol eder."""
    return username == VALID_USERNAME and password == VALID_PASSWORD

def authenticate():
    """Temel kimlik doğrulamayı isteyen bir 401 yanıtı gönderir."""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    """Kimlik doğrulaması gerektiren bir decorator."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
# --- Kimlik Doğrulama Mantığı Bitişi ---


# Endpoint'ler
@app.route('/person', methods=['POST'])
@requires_auth
def add_person():
    try:
        data = request.get_json()
        if not data:
            return create_response({"error": "Invalid JSON or missing request body"}, 400)

        name = data.get('name')
        surname = data.get('surname')
        age = data.get('age')

        if name is None or surname is None or age is None:
            return create_response({"error": "Missing required fields: 'name', 'surname', and 'age' are required"}, 400)

        if not isinstance(age, int) or age < 0:
            return create_response({"error": "Invalid age: must be a non-negative integer"}, 400)

        # Aynı isim ve soyisimde bir kişi olup olmadığını kontrol et
        existing_person = Person.query.filter_by(name=name, surname=surname).first()
        if existing_person:
            return create_response({"error": "Bu isim ve soyisimde bir kişi zaten mevcut"}, 409)

        new_person = Person(name=name, surname=surname, age=age)
        db.session.add(new_person)
        db.session.commit()
        person_data = {"id": new_person.id, "name": new_person.name, "surname": new_person.surname, "age": new_person.age}
        return create_response({"message": "Person added successfully", "person": person_data}, 201)

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error adding person: {e}")
        return create_response({"error": "An internal server error occurred"}, 500)

@app.route('/people', methods=['GET'])
@requires_auth
def get_people():
    try:
        people = Person.query.all()
        people_list = [{"id": person.id, "name": person.name, "surname": person.surname, "age": person.age} for person in people]
        return create_response({"people": people_list}, 200)

    except Exception as e:
        app.logger.error(f"Error getting people: {e}")
        return create_response({"error": "An internal server error occurred"}, 500)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Veritabanı tablolarını oluştur
    app.run(debug=True)