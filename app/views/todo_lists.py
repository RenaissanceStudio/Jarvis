from datetime import datetime

from flask import Blueprint, flash, redirect, request, render_template, url_for
from flask_login import login_required, current_user

from app import csrf
from app.model import Todo, db

todo_list = Blueprint('todo_list', __name__)


@todo_list.route('/', methods=['GET', 'POST'])
@login_required
def index():
    items = Todo.query.filter(Todo.author_id == current_user.id).all()
    return render_template('todo_list.html', entries=items, current_time=datetime.utcnow())


@csrf.exempt
@todo_list.route('/add', methods=['POST'])
@login_required
def add_item():
    td = Todo(request.form['title'], current_user.id)
    db.session.add(td)
    db.session.commit()

    flash('new entry added successfully')
    return redirect(url_for('todo_list.index'))


@csrf.exempt
@todo_list.route('/del/<int:id>', methods=['POST'])
@login_required
def del_item(id):
    print("delete item %d" % id)

    td = Todo.query.filter_by(id=id).first()
    db.session.delete(td)
    db.session.commit()

    return redirect(url_for('todo_list.index'))
