from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import pandas as pd
import sqlite3, json

from db import connect

def get_student_id(value):
    c = connect()
    id = c.execute("SELECT id FROM student WHERE id=?", (value,))
    return id


def get_item_id(value):
    c = connect()
    id = c.execute("SELECT id FROM item WHERE item=?", (value,))
    c.close()
    return id

app = Flask(__name__)
# Routes
@app.route('/') # Homepage
def index():
    c = connect()

    s = c.execute("SELECT * FROM student")
    return render_template("index.html", students=s)

@app.route('/student/<id>') # go to specific student
def student(id):
    c= connect()
    student = pd.read_sql_query("SELECT s.name, i.item",c)

    return render_template('student.html', student=student, checkedOut=checkedOut)

@app.route('/item/<item_id>') # go to specific item
def item(item_id):
    c = connect()
    i = c.execute("SELECT * FROM item WHERE id = ?", (item_id,)).fetchone()
    return render_template('item.html', item=item, data=i)

@app.route('/checkout', methods=("GET", "POST")) # Add new item
def checkout():
    if request.method == 'POST':
        name = request.form['name']
        item   = request.form['item']

        student_id = get_student_id(name)
        item_id = get_item_id(item)

        c = connect()
        c.execute("INSERT INTO checkout (student_id, item_id) VALUES(?,?)", (student_id, item_id)) # insert into chekout table
        c.commit()
        c.close()

        return redirect(url_for('index'))
    return render_template('checkout.html')

@app.route('/checkin', methods=("GET", "POST")) # Add new item
def checkin():
    if request.method == 'POST':
        name = request.form['name']
        item   = request.form['item']

        c = connect()
        c.execute("INSERT INTO checkin (item, name) VALUES(?,?)", (item,name)) # insert into chekout table
        c.execute("DELETE FROM checkout WHERE item=?", (item,))
        c.commit()
        c.close()

        return redirect(url_for('index'))
    return render_template('checkin.html')

@app.route('/create', methods=("GET", "POST")) # Add new item
def create():
    if request.method == 'POST':
        name = request.form['name']
        type   = request.form['type']


        c = connect()
        c.execute("INSERT INTO item (item, type) VALUES(?,?)", (name,type)) # insert into items table
        c.commit()

        return redirect(url_for('index'))
    return render_template('create.html')

@app.route("/delete/item/<id>") # Delete item
def delete_item(id):
    # TODO delete item from db
    return redirect(url_for('index'))

@app.route("/delete/student/<id>") # Delete item
def delete_student(id):
    # TODO delete item from db
    return redirect(url_for('index'))