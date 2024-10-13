from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), default='pending')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if 'title' not in data or not data['title']:
        return jsonify({"error": "O título da tarefa é obrigatório!"}), 400

    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({"error": "Tarefa não encontrada!"}), 404

    task.status = 'complete' if data.get('status') == 'complete' else 'pending'
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({"error": "Tarefa não encontrada!"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarefa removida com sucesso!"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
