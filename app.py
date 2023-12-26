from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {Todo.id} {Todo.description}>'
    
with app.app_context():
    db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description':  todo.description
    })
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())


app.run(debug=True)
