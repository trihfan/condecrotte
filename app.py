from flask import Flask, render_template, session, request, url_for, redirect, Markup
from datetime import datetime, date, time, timedelta
from pymongo import MongoClient
import os

# Run the app
app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

client = MongoClient(os.environ['MONGODB_URL'])
toilets = client.condecrotte.toilets
toilets.replace_one({"id": "toilet-w-1"}, {"id": "toilet-w-1", "name": "Toilette Femme 1"}, upsert=True)
toilets.replace_one({"id": "toilet-w-2"}, {"id": "toilet-w-2", "name": "Toilette Femme 2"}, upsert=True)
toilets.replace_one({"id": "toilet-w-3"}, {"id": "toilet-w-3", "name": "Toilette Femme 3"}, upsert=True)
toilets.replace_one({"id": "toilet-w-4"}, {"id": "toilet-w-4", "name": "Toilette Femme 4"}, upsert=True)
toilets.replace_one({"id": "toilet-w-5"}, {"id": "toilet-w-5", "name": "Toilette Femme 5 (Handicap)"}, upsert=True)

toilets.replace_one({"id": "toilet-m-1"}, {"id": "toilet-m-1", "name": "Toilette Homme 1"}, upsert=True)
toilets.replace_one({"id": "toilet-m-2"}, {"id": "toilet-m-2", "name": "Toilette Homme 2"}, upsert=True)
toilets.replace_one({"id": "toilet-m-3"}, {"id": "toilet-m-3", "name": "Toilette Homme 3"}, upsert=True)
toilets.replace_one({"id": "toilet-m-4"}, {"id": "toilet-m-4", "name": "Toilette Homme 4"}, upsert=True)
toilets.replace_one({"id": "toilet-m-5"}, {"id": "toilet-m-5", "name": "Toilette Homme 5 (Handicap)"}, upsert=True)

# Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    # Authentication
    if not 'username' in session:
        return redirect(url_for("login"))

    # Connect DB
    client = MongoClient(os.environ['MONGODB_URL'])
    toilets = client.condecrotte.toilets
    reservations = client.condecrotte.reservations

    # Handle reservation
    if request.method == 'POST':
        for id, hour in request.form.items():
            reservations.insert_one({ "date": date.today().strftime("%Y/%M/%d"), "id": id[5:], "time": hour, "user": session['username'] })

    # Load plan
    file = open('static/image/plan.svg', mode='r')
    plan = file.read()
    file.close()

    # Load toilet
    toilets_list = list(toilets.find())

    # Load reservation
    for toilet in toilets_list:
        toilet["disabled"] = list(reservations.find({ "date": date.today().strftime("%Y/%M/%d"), "id": toilet["id"] }))

    return render_template("index.html",
                           date=datetime.today().strftime('%I:%M %p, %a/%-d/%b/%Y'),
                           user=session['username'],
                           toilets=toilets_list,
                           plan=Markup(plan))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for("index"))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(host="localhost")
