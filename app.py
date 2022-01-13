from datetime import datetime
from os import replace
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import pandas as pd
import sqlite3, json, time

from db import connect

time.strftime('%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
app.secret_key = "test"

# Routes
@app.route('/') # Homepage
def index():
    c = connect()

    s = c.execute("SELECT id,name FROM student")
    return render_template("index.html", students=s)

@app.route('/student/<id>') # go to specific student
def student(id):
    c= connect()
    student = c.execute("SELECT s.id,i.id AS item_id,i.name AS item,i.statusDate,s.name AS student FROM student s LEFT JOIN item i on s.id=i.student_id WHERE s.id=?",(id,))
    return render_template('student.html', student=student)

@app.route("/items")
def items():
    c = connect()
    data = c.execute("SELECT i.id,i.name,s.name AS student FROM item i LEFT JOIN student s ON s.id=i.student_id")
    return render_template("items.html", data=data)

@app.route('/item/<id>') # go to specific item
def item(id):
    c = connect()
    i = c.execute("SELECT i.id,i.name,i.type,s.name AS student FROM item i LEFT JOIN student s ON s.id=i.student_id WHERE i.id=?", (id,)).fetchone()
    return render_template('item.html', item=i)

@app.route('/create/item', methods=("GET", "POST")) # Add new item
def create_item():
    if request.method == 'POST':
        c = connect()
        f = request.files["file"]
        f.save("db/item.csv")
        df = pd.read_csv("db/item.csv")
        df.to_sql("item", c, if_exists="replace")
        flash("Successfully added new items", "success")
        return redirect(url_for('index'))
    return render_template('create_item.html')

@app.route('/create/student', methods=("GET", "POST")) # Add new student
def create_student():
    if request.method == 'POST':
        c = connect()
        f = request.files["file"]
        f.save("db/student.csv")
        df = pd.read_csv("db/student.csv")
        df.to_sql("student", c, if_exists="replace")
        flash("Successfully added new students", "success")
        return redirect(url_for('index'))
    return render_template('create_student.html')

@app.route("/checkout", methods=("GET", "POST"))
def checkout():
    c = connect()
    if request.method == 'POST':
        name = request.form["name"]
        items = request.form["ids"]

        student_id = c.execute("SELECT id FROM student WHERE name=?", (name,)).fetchone()

        items=items.split(",")

        for i in items:
            c.execute("UPDATE item SET status='Out', student_id=?, statusDate=? WHERE id=?",(student_id["id"],datetime.now(),i))
            c.commit()

        flash("Successfully checked out items for "+name, "success")
        return redirect(url_for('index'))

    names = c.execute("SELECT name from student DESC").fetchall()
    return render_template('checkout.html', names=names)

@app.route("/checkin", methods=("GET", "POST"))
def checkin():
    c = connect()
    if request.method == 'POST':
        items = request.form["ids"]

        items=items.split(",")

        for i in items:
            c.execute("INSERT INTO checkin(student_id, item_id, dateOut) SELECT student_id, id, statusDate FROM item WHERE id=?;", (i,))
            c.execute("UPDATE item SET status='In', student_id=NULL, statusDate=? WHERE id=?",(datetime.now(),i))
            c.commit()

        flash("Successfully checked in items", "success")
        return redirect(url_for('index'))

    names = c.execute("SELECT name from student DESC").fetchall()
    return render_template('checkin.html', names=names)

@app.route("/scan")
def scan():
    code = request.args.get("code", type=str)
    action = request.args.get("action", type=int)
    itemStatus=True
    items=[]
    if code:
        c = connect()
        if(action == 1):
            items = c.execute("SELECT name, id FROM item WHERE status='In' AND code=?;", (code,)).fetchone()
        elif(action == 0):
            items = c.execute("SELECT name, id FROM item WHERE status!='In' AND code=?;", (code,)).fetchone()
        if(items == None):
            itemStatus=False
            return jsonify(result="", item_id=0, itemStatus=itemStatus)

    return jsonify(result=items["name"],item_id=items["id"], itemStatus=itemStatus)