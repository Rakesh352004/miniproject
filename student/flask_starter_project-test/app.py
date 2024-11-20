from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Reddy%4096320@localhost:5433/amazon_app'

db = SQLAlchemy(app)


class student(db.Model):
    USN = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Sem = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    data = student.query.all()
    context = []
    for dt in data:
        dd = {"USN": dt.USN, "Name": dt.Name, "Sem": dt.Sem, "course": dt.course,"phone_no": dt.phone_no}
        context.append(dd)
    print(context)
    # print("data: {}".format(data))
    return render_template('todo.html', todo=context)


@app.route('/add-task')
def add_task():
    return render_template('add_task.html')


@app.route('/submit', methods=['POST'])
def create_user():
    Name = request.form['Name']
    Sem = request.form['Sem']
    course = request.form['course']
    phone_no=request.form['phone_no']
    print(f"Name is: {Name}, Sem is: {Sem}, and course is: {course},phone_no is: {phone_no}")
    new_task = student(Name=Name, Sem=Sem, course=course,phone_no=phone_no)
    print("new_task: {}".format(new_task))
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('add_task'))


@app.route('/delete/<int:USN>', methods=['GET', 'DELETE'])
def delete_user(USN):
    Name = student.query.get(USN)
    print("Name: {}".format(Name))

    if not Name:
        return jsonify({'message': 'task not found'}), 404
    try:
        db.session.delete(Name)
        db.session.commit()
        return jsonify({'message': 'task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500


@app.route('/update_task/<int:USN>', methods=['GET', 'POST'])
def update_task(USN):
    Name = student.query.get_or_404(USN)
    print(Name.USN)
    if not Name:
        return jsonify({'message': 'task not found'}), 404

    if request.method == 'POST':
        Name.Name = request.form['Name']
        Name.Sem = request.form['Sem']
        Name.course = request.form['course']
        Name.phone_no=request.form['phone_no']

        try:
            db.session.commit()
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            return "there is an issue while updating the record"
    return render_template('update.html', task=Name)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
