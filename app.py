from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import pandas as pd
import sqlite3, json

from db import connect

app = Flask(__name__)
# Routes
@app.route('/') # Homepage
def index():
    c = connect()

    s = c.execute("SELECT * FROM student")
    return render_template("index.html", students=s)

@app.route("/items")
def items():
    c = connect()

    data = c.execute("SELECT i.id,i.name,s.name AS student FROM item i LEFT JOIN checkout c on i.id=c.item_id LEFT JOIN student s ON s.id=c.student_id")
    return render_template("items.html", data=data)

@app.route('/student/<id>') # go to specific student
def student(id):
    c= connect()
    student = c.execute("SELECT s.id,i.id AS item_id,i.name AS item,c.dateOut,s.name AS student FROM student s LEFT JOIN checkout c on s.id=c.student_id LEFT JOIN item i ON i.id=c.item_id WHERE s.id=?",(id,))
    return render_template('student.html', student=student)

@app.route('/item/<id>') # go to specific item
def item(id):
    c = connect()
    i = c.execute("SELECT * FROM item WHERE id = ?", (id,)).fetchone()
    return render_template('item.html', item=i)


@app.route('/create/item', methods=("GET", "POST")) # Add new item
def create_item():
    if request.method == 'POST':
        name = request.form['name']
        type   = request.form['type']


        c = connect()
        c.execute("INSERT INTO item (item, type) VALUES(?,?)", (name,type)) # insert into items table
        c.commit()

        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/create/student', methods=("GET", "POST")) # Add new student
def create_student():
    if request.method == 'POST':
        c = connect()
        df = pd.read_csv(request.files.get('file'))
        df.to_sql("student", c)
        return redirect(url_for('index'))
    return render_template('create_student.html')

@app.route("/delete/item/<id>") # Delete item
def delete_item(id):
    # TODO delete item from db
    return redirect(url_for('index'))

@app.route("/delete/student/<id>") # Delete item
def delete_student(id):
    # TODO delete item from db
    return redirect(url_for('index'))