import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env as config

from bson.objectid import ObjectId

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'aroundTheWorldRace'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html",
                           clues=mongo.db.clues.find({"leg": "1"}).sort("step"),
                           teams=mongo.db.teams.find().sort("time"))


@app.route('/join_game', methods=["POST"])
def join_game():
    teams = mongo.db.teams
    team_doc = {'team_name': request.form.get('team_name'), 'time': '000'}
    teams.insert_one(team_doc)
    return redirect(url_for('stage_1'))


@app.route('/stage_1')
def stage_1():
    return render_template("stage-1.html",
                           clues=mongo.db.clues.find({"leg": "1"}).sort("step"),
                           teams=mongo.db.teams.find().sort("time"))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
