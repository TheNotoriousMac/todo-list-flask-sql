from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
Bootstrap5(app)

db = SQLAlchemy()

db.init_app(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_text = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Todo {self.todo_text}>'

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    result = db.session.execute(db.select(Todo).order_by(Todo.id))
    all_todos = result.scalars().all()

    # db.session.commit()
    return render_template("index.html", todos=all_todos)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        new_todo = Todo(
           todo_text = request.form['todo_text']
        )
        db.session.add(new_todo)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == "POST":
        todo_id = request.form['id']
        todo_to_update = db.get_or_404(Todo, todo_id)
        todo_to_update.todo_text = request.form['todo_text']
        db.session.commit()
        return redirect(url_for('home'))
    todo_id = request.args.get('id')
    todo_selected = db.get_or_404(Todo, todo_id)

    return render_template('edit.html', todo=todo_selected)


@app.route('/delete')
def delete():
    todo_id = request.args.get('id')
    todo_to_delete = db.get_or_404(Todo, todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)