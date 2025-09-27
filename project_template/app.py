from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pomodoro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        #добавление задачи
        title = request.form.get('title')
        description = request.form.get('description')
        if title:
            new_task = Task(title=title, description=description)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('about'))

    tasks = Task.query.all()
    return render_template('about.html', tasks=tasks)


@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('about'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('about'))


@app.route('/clear_completed')
def clear_completed():
    Task.query.filter_by(completed=True).delete()
    db.session.commit()
    return redirect(url_for('about'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)