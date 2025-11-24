import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():

    birthdays = db.execute("SELECT * FROM birthdays")

    if request.form.get("search"):
        search = request.form.get("search")
        return redirect("/characters", search=search)

    return render_template("index.html", birthdays=birthdays)



@app.route("/characters", methods=["GET", "POST"])
def characters():

        search = request.form.get("search")

        searchings = db.execute("SELECT * FROM birthdays WHERE id = ? OR name LIKE ?", search, search)

        if request.form.get('sendEdits') == 'Send Edits':
            editName = request.form.get("editName")
            editBirthdate = request.form.get("editBirthdate")
            editBirthplace = request.form.get("editBirthplace")

            db.execute("UPDATE birthdays SET name = ?, birthdate = ?, birthplace = ? WHERE name LIKE ? OR id = ?", editName, editBirthdate, editBirthplace, search, search)
            updates = db.execute("SELECT * FROM birthdays WHERE name LIKE ? OR id = ?", search, search)

            return render_template("characters.html", searchings=updates, search=search)

        elif request.form.get('confirmButton') == 'Confirm':
            search = request.form.get("search")

            db.execute("DELETE FROM birthdays WHERE name LIKE ? OR id = ?", search, search)
            updates = db.execute("SELECT * FROM birthdays WHERE name LIKE ? OR id = ?", search, search)

            return render_template("characters.html", searchings=updates, search=search)

        elif request.form.get('Add') == 'Add':
            name = request.form.get("name")

            birthdate = request.form.get("birthdate")


            birthplace = request.form.get("birthplace")
            db.execute("INSERT INTO birthdays (name, birthdate, birthplace) VALUES(?, ?, ?)", name, birthdate, birthplace)
            updates = db.execute("SELECT * FROM birthdays WHERE name LIKE ? OR id = ?", name, name)

            return render_template("characters.html", searchings=updates, search=search)
        else:
             return render_template("characters.html", searchings=searchings, search=search)


