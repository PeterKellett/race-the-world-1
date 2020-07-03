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
    return render_template("home.html", clues=mongo.db.clues.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
