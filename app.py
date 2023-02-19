from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# live back-end server: https://one90223-web1-project.onrender.com/students


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)


@app.route('/students')
def get():
    res = []
    for stu in Students.query.all():
        res.append({'id': stu.id, 'name': stu.name, 'age': stu.age})
    return jsonify(res)

@app.route('/students', methods=['POST'])
def post():
    data = request.get_json()
    student = Students(name=data['name'], age=data['age'])
    db.session.add(student)
    db.session.commit()
    return jsonify({'id': student.id})

@app.route('/students/<int:stu_id>', methods=['PUT'])
def put(stu_id):
    stu = Students.query.get(stu_id)
    if not stu:
        return jsonify({'error': 'Student Not Found'}), 404
    else:
        data = request.get_json()
        stu.name = data['name']
        stu.age = data['age']
        db.session.commit()
        return jsonify({'id': stu.id})
    
@app.route('/students/<int:stu_id>')
def get_single(stu_id):
    stu = Students.query.get(stu_id)
    if not stu:
        return jsonify({'error': 'Student Not Found'}), 404
    else:
        return jsonify({'id': stu.id, 'name': stu.name, 'age': stu.age})
    
@app.route('/students/<int:stu_id>', methods=['DELETE'])
def delete(stu_id):
    stu = Students.query.get(stu_id)
    if not stu:
        return jsonify({'error': 'Student Not Found'}), 404
    else:
        db.session.delete(stu)
        db.session.commit()
        return jsonify({'result': f'Student {stu.name} Deleted.'})





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)