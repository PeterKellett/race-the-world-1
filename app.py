import os
from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env as config

from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "randomstring123")

app.config["MONGO_DBNAME"] = 'aroundTheWorldRace'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


def start_time(username):
    now = datetime.now().strftime("%H:%M:%S")
    print(now)
    return redirect(url_for('stage_1', username=session["username"]))


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        teams = mongo.db.teams
        team_doc = {'team_name': request.form.get('team_name'), 'time': '000'}
        teams.insert_one(team_doc)
        session["username"] = request.form["team_name"]
        return redirect(url_for('stage_1', username=session["username"]))
    else:
        return render_template("home.html",
                               clues=mongo.db.clues.find({"leg": "1"}).sort("step"),
                               teams=mongo.db.teams.find().sort("time"))


@app.route('/stage_1')
def stage_1():
    return render_template("stage-1.html",
                           clues=mongo.db.clues.find({"leg": "1"}).sort("step"),
                           teams=mongo.db.teams.find().sort("time"),
                           username=session["username"])


@app.route("/update_time/<team_id>", methods=["POST"])
def update_time(team_id):
    mongo.db.teams.update(
        {'_id': ObjectId(team_id)},
        {'time': request.form.get('time')})
    return redirect(url_for('stage_2'))


@app.route('/stage_2')
def stage_2():
    return render_template("stage-2.html",
                           clues=mongo.db.clues.find({"leg": "2"}).sort("step"),
                           teams=mongo.db.teams.find().sort("time"))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
